from django.contrib import admin

# Register your models here.
from capstone.models import User, Person, Organisation, Event, TicketedEvent, Category

admin.site.register(User)
admin.site.register(Person)
admin.site.register(Organisation)
admin.site.register(Event)
admin.site.register(TicketedEvent)
admin.site.register(Category)
