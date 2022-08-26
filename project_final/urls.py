from django.urls import include, path
from django.contrib import admin
from capstone.views import capstone, persons, organisations
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('capstone.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', capstone.sign_up, name='signup'),
    path('accounts/signup/person/', persons.person_sign_up, name='person_signup'),
    path('accounts/signup/organisation/', organisations.org_sign_up, name='organisation_signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)