from django.conf.urls import patterns, url


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from dms.api.rapid_pro_endpoint import RapidProListCreateView
from dms.api.location_endpoint import LocationListCreateView
from dms.api.mobile_user_endpoint import MobileUserListCreateView
from dms.views.homepage import HomeView


urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view()),
    # url(r'^necoc/', include('necoc.foo.urls')),

    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/rapid-pro/$', RapidProListCreateView.as_view()),
    url(r'^api/v1/locations/$', LocationListCreateView.as_view()),
    url(r'^api/v1/mobile-users/$', MobileUserListCreateView.as_view()),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

