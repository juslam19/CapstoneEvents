from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.utils import timezone

class User(AbstractUser):
    is_person = models.BooleanField()


class Category(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#fc0000')

    def get_html_badge(self):
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' \
               % (escape(self.color), "CATEGORY: " + escape(self.name))
        return mark_safe(html)

    def __str__(self):
        return self.name


class Organisation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to = "images/", default="../static/img/person.jpg")
    name = models.CharField(max_length=500, unique=True)
    about = models.CharField(max_length=10000)
    mobile = models.CharField(max_length=20)
    hq = models.CharField(max_length=500)
    color = models.CharField(max_length=500, default='#4800ff')

    def get_html_badge(self):
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' \
               % (escape(self.color), "ORG: " + escape(self.name))
        return mark_safe(html)


class Event(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=500, unique=True, blank=False)
    image = models.ImageField(upload_to = "images/", blank=False)
    likes = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events', blank=False)
    about = models.CharField(max_length=10000, blank=False)
    capacity = models.PositiveIntegerField(default=0, blank=False)
    booked = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)
    updated = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)
    update_no = models.PositiveIntegerField(default=0)

    def serialize(self):
        return {
            "likes": self.likes
        }



class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to = "images/", default="../static/img/person.jpg")
    name = models.CharField(max_length=500)
    mobile = models.CharField(max_length=20)
    events = models.ManyToManyField(Event, through='TicketedEvent')
    interests = models.ManyToManyField(Category, related_name='interested_persons')


class TicketedEvent(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='ticketed_events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticketed_events')
    booking_date = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
