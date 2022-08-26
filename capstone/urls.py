from django.urls import include, path

from .views import capstone, persons, organisations

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',  capstone.home, name='home'),
    path("like/<str:event_id>", persons.like, name="like"),
    path("like_helper/<str:event_id>", persons.like_helper, name="like_helper"),


    path('persons/', include(([
        path('', persons.event_list, name='event_list'),
        path('all/', persons.all_list, name='all_list'),
        path('interests/', persons.person_interests, name='person_interests'),
        path('ticketed/', persons.ticketed_event_list, name='ticketed_event_list'),
        path('ended/', persons.ended_event_list, name='ended_event_list'),
        path('past/', persons.past_event_list, name='past_event_list'),
        path('event/<int:pk>/', persons.details, name='details'),
        path('event/<int:pk>/get_ticket', persons.get_ticket, name='get_ticket'),
        path('event/<int:pk>/view_ticket', persons.view_ticket, name='view_ticket'),
        path('organisation/', persons.org_list, name='org_list'),
        path('organisation/<int:pk>/profile', persons.org_profile, name='org_profile'),
        path('profile', persons.profile, name='profile'),
        path('search_list', persons.search, name='search_list'),
    ], 'capstone'), namespace='persons')),

    path('organisations/', include(([
        path('', organisations.event_change_list, name='event_change_list'),
        path('ended/', organisations.ended_list, name='ended_change_list'),
        path('event/add/', organisations.event_create, name='event_add'),
        path('event/<int:pk>/edit', organisations.event_edit, name='event_edit'),
        path('event/<int:pk>/results/', organisations.event_results, name='event_results'),
        path('profile', organisations.org_profile, name='profile'),
        path('person/<int:pk>/profile', organisations.profile, name='person_profile'),
        path('event/<int:pk>/', organisations.details, name='details'),
        path('event/<int:pk>/delete/', organisations.delete, name='delete'),
    ], 'capstone'), namespace='organisations')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)