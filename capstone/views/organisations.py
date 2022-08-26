from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from ..decorators import organisation_required
from ..forms import OrganisationSignUpForm, EventCreateForm, EventEditForm
from ..models import User, Organisation, Person, Event, Category, TicketedEvent
from django.core.exceptions import ValidationError

def org_sign_up(request):

    user_type = 'organisation'
    form = OrganisationSignUpForm()

    if request.method == "POST":
        filled_form = OrganisationSignUpForm(request.POST, request.FILES)

        # Attempt to create new user
        if filled_form.is_valid():
            user = filled_form.save()
            login(request, user)
            messages.success(request, f'Successfully created account! Welcome to CapstoneEvents, '
                                      + f'{user.organisation.name}.')
            return redirect('organisations:event_change_list')

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
@organisation_required
def event_change_list(request):

    organisation = request.user.organisation
    events = Event.objects.filter(organisation=organisation) \
        .filter(end_time__gte=timezone.now()) \
        .order_by('start_time')

    return render(request, 'capstone/organisations/event_change_list.html', {
        'events': events
    })


@login_required
@organisation_required
def ended_list(request):

    organisation = request.user.organisation
    events = Event.objects.filter(organisation=organisation) \
        .filter(end_time__lt=timezone.now()) \
        .order_by('start_time')

    return render(request, 'capstone/organisations/ended_change_list.html', {
        'events': events
    })


@login_required
@organisation_required
def event_create(request):

    form = EventCreateForm()

    if request.method == "POST":

        name = request.POST.get("name")
        image = request.FILES.get('image')
        category_pk = request.POST.get("category")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        about = request.POST.get("about")
        capacity = request.POST.get("capacity")
        organisation = request.user.organisation

        form = EventCreateForm(request.POST, request.FILES)

        if form.is_valid():
            category = Category.objects.get(pk=category_pk)

            try:
                form.valid_date()
                Event(name=name, image=image, category=category, start_time=start_time,end_time=end_time,
                      about=about, capacity=capacity, organisation=organisation).save()
                messages.success(request, f'Event {name} successfully created.')
                return redirect('organisations:event_change_list')

            except ValidationError as errors:
                messages.info(request, "For security purposes, image is not kept after reload.")
                for e in errors:
                    messages.warning(request, e)

        else:
            messages.info(request, "For security purposes, image is not kept after reload.")
            messages.warning(request, form.errors)

    return render(request, 'capstone/organisations/event_add_form.html', {
            'form': form
        })


@login_required
@organisation_required
def event_edit(request, pk):

    event = Event.objects.get(pk=pk)
    form = EventEditForm(instance=event)
    is_owner = Event.objects.get(pk=pk).organisation == request.user.organisation

    messages.info(request, "Image can be left blank -- Original Image will be used.")

    if request.method == "POST":

        if request.FILES.get('image') is None:
            image = event.image
        else:
            image = request.FILES.get('image')
        category_pk = request.POST.get("category")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        about = request.POST.get("about")
        capacity = request.POST.get("capacity")

        if request.FILES.get('image') is None:
            form = EventEditForm(request.POST, {'image' : event.image})
        else:
            form = EventEditForm(request.POST, request.FILES)

        if form.is_valid():

            if request.FILES.get('image') is not None:
                # removes image FILE from database
                event.image.delete(False)
                # then updates model with new image FILE AND path
                event.image = image;

            event.category = Category.objects.get(pk=category_pk)
            event.about = about
            event.capacity = capacity

            try:
                form.valid_date(request.POST)
                event.start_time = start_time
                event.end_time = end_time

            except ValidationError as errors:
                messages.info(request, "For security purposes, image is not kept after reload.")
                for e in errors:
                    messages.warning(request, e)

                return render(request, 'capstone/organisations/event_edit_form.html', {
                    'form': form,
                    'event': event,
                    'is_owner': is_owner
                })

            event.updated = timezone.now()
            event.update_no += 1
            event.save()

            messages.success(request, f'Event {event.name} successfully edited.')
            return redirect('organisations:details', event.pk)

        else:
            messages.info(request, "For security purposes, image is not kept after reload.")
            messages.warning(request, form.errors)

    return render(request, 'capstone/organisations/event_edit_form.html', {
        'form': form,
        'event': event,
        'is_owner': is_owner
    })


@login_required
@organisation_required
def event_results(request, pk):

    event = get_object_or_404(Event, pk=pk)
    ticketed_events = event.ticketed_events.select_related('person__user').order_by('-booking_date')
    total_ticketed_events = ticketed_events.count()

    is_owner = event.organisation == request.user.organisation

    return render(request, 'capstone/organisations/event_results.html', {
        'ticketed_events': ticketed_events,
        'total_ticketed_events': total_ticketed_events,
        'event': event,
        'is_owner': is_owner
    })

@login_required
@organisation_required
def org_profile(request):

    organisation = request.user.organisation
    events = Event.objects.filter(organisation=organisation)

    return render(request, 'capstone/org_profile.html', {
        'organisation': organisation,
        'events': events
    })

@login_required
@organisation_required
def profile(request, pk):

    person = get_object_or_404(Person, pk=pk)

    is_involved = person.events.filter(organisation=request.user.organisation).count() > 0

    return render(request, 'capstone/profile.html', {
        'person': person,
        'is_involved': is_involved
    })


@login_required
@organisation_required
def details(request, pk):

    previous_page = request.META['HTTP_REFERER']

    event = get_object_or_404(Event, pk=pk)
    event.booked = TicketedEvent.objects.filter(event=event).count()
    event.save()

    return render(request, 'capstone/event_details.html', {
        'event': event,
        'previous_page': previous_page
    })

@login_required
@organisation_required
def delete(request, pk):
    get_object_or_404(Event, pk=pk).delete()
    return redirect('organisations:event_change_list')