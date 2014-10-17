from django.conf.urls import patterns, url


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from dms.api.bulk_sms_endpoint import SentMessageListCreateView
from dms.api.disaster_endpoint import DisasterListCreateView
from dms.api.disaster_type_endpoint import DisasterTypeListCreateView
from dms.api.location_stats_service_endpoint import LocationStatsListView
from dms.api.poll_endpoint import PollListCreateView
from dms.api.poll_response_endpoint import PollResponseListCreateView
from dms.api.rapid_pro_endpoint import RapidProListCreateView, RapidProRetrieveUpdateView
from dms.api.location_endpoint import LocationListCreateView
from dms.api.mobile_user_endpoint import MobileUserListCreateView
from dms.views.homepage import HomeView


urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view()),
    # url(r'^necoc/', include('necoc.foo.urls')),

    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/rapid-pro/$', RapidProListCreateView.as_view()),
    url(r'^api/v1/poll-responses/$', PollResponseListCreateView.as_view()),
    url(r'^api/v1/rapid-pro/(?P<id>[0-9a-z]+)/$', RapidProRetrieveUpdateView.as_view()),
    url(r'^api/v1/locations/$', LocationListCreateView.as_view()),
    url(r'^api/v1/polls/$', PollListCreateView.as_view()),
    url(r'^api/v1/mobile-users/$', MobileUserListCreateView.as_view()),
    url(r'^api/v1/sent-messages/$', SentMessageListCreateView.as_view()),
    url(r'^api/v1/disaster-types/$', DisasterTypeListCreateView.as_view()),
    url(r'^api/v1/disasters/$', DisasterListCreateView.as_view()),
    url(r'^api/v1/location-stats/$', LocationStatsListView.as_view()),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

