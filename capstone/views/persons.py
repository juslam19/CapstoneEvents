import json
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from ..decorators import person_required
from ..forms import PersonInterestsForm, PersonSignUpForm, CategoryForm
from ..models import User, Person, Organisation, Event, Category, TicketedEvent, Like
from django.core.exceptions import ValidationError

@login_required
@person_required
def person_interests(request):

    person = request.user.person
    pk_list = list(pk for pk in person.interests.values_list('pk', flat=True))
    interests = { 'interests' : pk_list }
    form = PersonInterestsForm(interests)

    if request.method == "POST":

        filled_form = PersonInterestsForm(request.POST)

        if filled_form.is_valid():
            messages.success(request, 'Interests updated with success!')
            person.interests.set(request.POST.getlist('interests'))
            return redirect('persons:event_list')
        else:
            messages.warning(request, 'At least one interest needs to be selected.')
            return render(request, 'capstone/persons/interests_form.html', {
                'form': filled_form
            })

    else:

        return render(request, 'capstone/persons/interests_form.html', {
            'form': form
        })


def person_sign_up(request):

    user_type = 'person'
    form = PersonSignUpForm()

    if request.method == "POST":
        filled_form = PersonSignUpForm(request.POST, request.FILES)

        # Attempt to create new user
        if filled_form.is_valid():
            user = filled_form.save()
            login(request, user)
            messages.success(request, f'Successfully created account! Welcome to CapstoneEvents, '
                             + f'{user.person.name}.')
            return redirect('persons:event_list')

        else:
            messages.info(request, "For security purposes, image is not kept after reload.")
            return render(request, 'registration/signup_form.html', {
                'user_type': user_type,
                'form': filled_form
            })

    else:
        return render(request, 'registration/signup_form.html', {
            'user_type': user_type,
            'form': form
        })


@login_required
@person_required
def ticketed_event_list(request):

    ticketed_events = request.user.person.ticketed_events \
        .filter(event__end_time__gte=timezone.now()) \
        .select_related('event', 'event__category') \
        .order_by('event__start_time')

    return render(request, "capstone/persons/ticketed_event_list.html", {
        'ticketed_events': ticketed_events
    })

@login_required
@person_required
def ended_event_list(request):

    ticketed_events = request.user.person.ticketed_events \
        .filter(event__end_time__lt=timezone.now()) \
        .select_related('event', 'event__category') \
        .order_by('event__start_time')

    return render(request, "capstone/persons/ended_event_list.html", {
        'ticketed_events': ticketed_events
    })

@login_required
@person_required
def details(request, pk):
    event = get_object_or_404(Event, pk=pk)
    person = request.user.person
    previous_page = request.META['HTTP_REFERER']

    unique_ticket = TicketedEvent.objects.filter(person=person, event=event).count()

    if unique_ticket == 0:
        button = 'Get Ticket'
    else:
        button = 'Cancel Ticket'

    event.booked = TicketedEvent.objects.filter(event=event).count()
    event.save()

    if event.end_time < timezone.now():
        ended = True
    else:
        ended = False

    return render(request, 'capstone/event_details.html', {
        'event': event,
        'person': person,
        'button': button,
        'ended': ended,
        'previous_page' : previous_page,
    })

@login_required
@person_required
def get_ticket(request, pk):

    event = get_object_or_404(Event, pk=pk)
    person = Person.objects.filter(user=request.user)[0]

    unique_ticket = TicketedEvent.objects.filter(person=person, event=event).count()

    if unique_ticket == 0:
        if event.capacity > event.booked:
            TicketedEvent.objects.create(person=person, event=event)
            messages.success(request, f'Event {event.name} ticketed with success!')
        else:
            messages.warning(request, f'Event {event.name} ticketing failed.')
    else:
        TicketedEvent.objects.filter(person=person, event=event).delete()
        messages.warning(request, f'Event {event.name} ticket cancelled with success.')
    event.booked = TicketedEvent.objects.filter(event=event).count()
    event.save()
    return redirect('persons:event_list')

@login_required
@person_required
def view_ticket(request, pk):
    event = get_object_or_404(Event, pk=pk)
    person = Person.objects.filter(user=request.user)[0]
    ticketed_event = TicketedEvent.objects.filter(person=person, event=event)[0]
    booking_date = ticketed_event.booking_date
    current_time = timezone.now()

    is_owner = ticketed_event.person.user == request.user

    return render(request, 'capstone/persons/event_ticket.html', {
        'event': event,
        'person': person,
        'booking_date': booking_date,
        'is_owner' : is_owner,
        'current_time' : current_time
    })

@login_required
@person_required
def org_profile(request, pk):
    organisation = get_object_or_404(Organisation, pk=pk)
    events = Event.objects.filter(organisation=organisation)

    return render(request, 'capstone/org_profile.html', {
        'organisation': organisation,
        'events': events
    })

@login_required
@person_required
def profile(request):
    person = request.user.person

    return render(request, 'capstone/profile.html', {
        'person': person
    })

@login_required
@person_required
@csrf_exempt
def like(request, event_id):
    if request.method == "PUT":
        uniqueLike = Like.objects.filter(person=request.user.person, event=Event.objects.get(id=event_id)).count()
        if json.loads(request.body).get("like"):
            if uniqueLike == 0:
                Like.objects.create(person=request.user.person, event=Event.objects.get(id=event_id))
        else:
            if uniqueLike == 1:
                Like.objects.filter(person=request.user.person, event=Event.objects.get(id=event_id)).delete()

        event = Event.objects.get(id=event_id)
        event.likes = Like.objects.filter(event=event).count()
        event.save()

    if request.method == "GET":
        return JsonResponse(Event.objects.get(id=event_id).serialize())

@login_required
@person_required
@csrf_exempt
def like_helper(request, event_id):
    if request.method == "GET":
        like_count = Like.objects.filter(person=request.user.person, event=Event.objects.get(id=event_id)).count()
        if like_count == 0 :
            return JsonResponse({ 'message':'error' })
        elif like_count == 1:
            return JsonResponse({ 'message':'success' })
        else:
            # DO NOTHING
            # For error checking ONLY
            return JsonResponse({ 'message':'SNAFU' })

@login_required
@person_required
def org_list(request):
    substring = request.GET.get('substring')

    if substring is None:
        substring = ""

    organisations = Organisation.objects.filter(name__icontains=str(substring)).order_by('name')

    return render(request, "capstone/persons/org_list.html", {
        "organisations": organisations,
        "substring": substring
    })

@login_required
@person_required
def search(request):

    form = CategoryForm

    substring = request.GET.get('substring')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    available = request.GET.get('available')
    past = request.GET.get('past')
    pks = request.GET.getlist('category')

    sort = request.GET.get('sort')

    # CHECK IF START TIME IS AT OR BELOW END TIME
    # BEFORE PROCESSING ANYTHING

    if sort is None:
        sort = '-likes'

    events = Event.objects.filter(category__pk__in=pks)

    if substring is None:
        substring = ""
    if start_time is None:
        start_time = ""
    if end_time is None:
        end_time = ""

    if available != "available" and past == "past":
        events = events.filter(end_time__lt=timezone.now())
    elif available == "available" and past != "past":
        events = events.filter(start_time__gte=timezone.now())
    elif available != "available" and past != "past":
        events = events.filter(end_time__lt=timezone.now()).filter(start_time__gte=timezone.now())
    else:
        events = events
        # DO NOTHING

    events = events.filter(name__icontains=str(substring))

    events = events.order_by(sort)

    try:
        if (start_time is not None and end_time is not None) and (start_time > end_time):
            raise ValidationError('End time must be at / after Start time. Searching without times.')

        else:
            if start_time == "" and end_time != "":
                events = events.filter(end_time__lte=end_time)
            elif start_time != "" and end_time == "":
                events = events.filter(start_time__gte=start_time)
            elif start_time != "" and end_time != "":
                events = events.filter(start_time__gte=start_time).filter(end_time__lte=end_time)
            else:
                events = events
                # DO NOTHING

            messages.success(request, 'Latest Search: {}'.format(timezone.now().strftime("%b %d, %Y, %H:%M:%S %p")))

    except ValidationError as errors:
        for e in errors:
            messages.warning(request, e)

    return render(request, "capstone/persons/search_list.html", {
        "events": events,
        "substring": substring,
        "start_time": start_time,
        "end_time": end_time,
        "available" : available,
        "past" : past,
        "categories": Category.objects.filter(pk__in=pks),
        "pks": pks,
        "form": form,
        'sort': sort
    })

@login_required
@person_required
def all_list(request):
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    person = request.user.person
    ticketed_events = person.ticketed_events.values_list('event', flat=True)
    events = Event.objects.exclude(pk__in=ticketed_events) \
        .filter(end_time__gte=timezone.now())

    if start_time is None:
        start_time = ""
    if end_time is None:
        end_time = ""

    sort = request.GET.get('sort')
    if sort is None:
        sort = '-likes'

    events = events.order_by(sort)

    try:
        if (start_time is not None and end_time is not None) and (start_time > end_time):
            raise ValidationError('End time must be at / after Start time. Searching without times.')
        else:
            if start_time == "" and end_time != "":
                events = events.filter(end_time__lte=end_time)
            elif start_time != "" and end_time == "":
                events = events.filter(start_time__gte=start_time)
            elif start_time != "" and end_time != "":
                events = events.filter(start_time__gte=start_time).filter(end_time__lte=end_time)
            else:
                events = events
                # DO NOTHING

    except ValidationError as errors:
        for e in errors:
            messages.warning(request, e)

    return render(request, "capstone/persons/all_list.html", {
        "events": events,
        "start_time": start_time,
        "end_time": end_time,
        'sort': sort
    })

@login_required
@person_required
def event_list(request):
    sort = request.GET.get('sort')
    if sort is None:
        sort = '-likes'
    person = request.user.person

    person_interests = person.interests.values_list('pk', flat=True)
    ticketed_events = person.ticketed_events.values_list('event', flat=True)

    events = Event.objects.filter(category__in=person_interests) \
        .filter(end_time__gte=timezone.now()) \
        .exclude(pk__in=ticketed_events) \
        .order_by(sort)

    return render(request, "capstone/persons/event_list.html", {
        'events': events,
        "sort": sort,
    })


@login_required
@person_required
def past_event_list(request):
    sort = request.GET.get('sort')
    if sort is None:
        sort = '-likes'
    person = request.user.person

    ticketed_events = person.ticketed_events.values_list('event', flat=True)

    events = Event.objects.all() \
        .filter(end_time__lt=timezone.now()) \
        .exclude(pk__in=ticketed_events) \
        .order_by(sort)

    return render(request, "capstone/persons/past_event_list.html", {
        'events': events,
        "sort": sort,
    })
