from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from capstone.models import User, Person, Organisation, Event, Category
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

class OrganisationSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    name = forms.CharField(label='Organisation Name', max_length=500)
    image = forms.ImageField()
    about = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':3, 'cols':5}), label='Company description', max_length=10000)
    mobile = forms.CharField(label='Contact Number', max_length=20)
    hq = forms.CharField(label='Company Location', max_length=500)

    def save(self):
        user = super().save(commit=False)
        user.is_person = False
        user.save()

        Organisation.objects.create(user=user,
           name=self.cleaned_data.get('name'),
           image=self.cleaned_data.get('image'),
           about=self.cleaned_data.get('about'),
           mobile=self.cleaned_data.get('mobile'),
           hq=self.cleaned_data.get('hq'))

        return user


class PersonSignUpForm(UserCreationForm):
    name = forms.CharField(label='Full Name', max_length=500)
    image = forms.ImageField()
    mobile = forms.CharField(label='Mobile Number', max_length=20)
    interests = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_person = True
        user.save()

        person = Person.objects.create(user=user, image=self.cleaned_data.get('image'), name=self.cleaned_data.get('name'), mobile=self.cleaned_data.get('mobile'))
        person.interests.add(*self.cleaned_data.get('interests'))

        return user


class PersonInterestsForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('category', )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label='',
    )


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'image', 'category', 'start_time', 'end_time', 'about', 'capacity', )

    name = forms.CharField(label='Event Name')
    image = forms.ImageField(label='Image')
    category = forms.ModelChoiceField(label='Category', queryset=Category.objects.all())
    start_time = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],
                                     widget = forms.DateTimeInput(
                                         attrs={'type': 'datetime-local'},
                                         format='%Y-%m-%d %H:%M'))
    end_time = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],
                                   widget = forms.DateTimeInput(
                                       attrs={'type': 'datetime-local'},
                                       format='%Y-%m-%d %H:%M'))
    about = forms.CharField(label='Description of event', widget=forms.Textarea)
    capacity = forms.IntegerField(label='Capacity', initial=0, validators=[MinValueValidator(0)])

    def valid_date(self):
        self.is_valid()
        cd = self.cleaned_data
        if cd['start_time'] > cd['end_time']:
            raise ValidationError("End Time must be at / after Start Time")


class EventEditForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('image', 'category', 'start_time', 'end_time', 'about', 'capacity', )

    image = forms.ImageField(label='Image')
    category = forms.ModelChoiceField(label='Category', queryset=Category.objects.all())
    start_time = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],
                                     widget = forms.DateTimeInput(
                                         attrs={'type': 'datetime-local'},
                                         format='%Y-%m-%dT%H:%M'))
    end_time = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],
                                   widget = forms.DateTimeInput(
                                       attrs={'type': 'datetime-local'},
                                       format='%Y-%m-%dT%H:%M'))
    about = forms.CharField(label='Description of event', widget=forms.Textarea)
    capacity = forms.IntegerField(label='Capacity', initial=0, validators=[MinValueValidator(0)])

    def valid_date(self, input):
        if input['start_time'] > input['end_time']:
            raise ValidationError("End Time must be at / after Start Time")


