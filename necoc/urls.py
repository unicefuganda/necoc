from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib.auth.decorators import login_required
from dms.api.bulk_sms_endpoint import SentMessageListCreateView
from dms.api.disaster_endpoint import DisasterListCreateView
from dms.api.disaster_type_endpoint import DisasterTypeListCreateView
from dms.api.location_stats_service_endpoint import LocationStatsListView, DistrictStatsListView
from dms.api.poll_endpoint import PollListCreateView
from dms.api.poll_response_endpoint import PollResponseListCreateView
from dms.api.rapid_pro_endpoint import RapidProListCreateView, RapidProRetrieveUpdateView
from dms.api.location_endpoint import LocationListCreateView
from dms.api.user_profile_endpoint import UserProfileListCreateView
from dms.views.api_token import ObtainAPIToken
from dms.views.export_poll_responses import ExportPollResponsesView
from dms.views.homepage import HomeView
from dms.views.login import Login, Logout


urlpatterns = patterns('',
    # Examples:
    url(r'^$', login_required(HomeView.as_view(), login_url='login/')),
    # url(r'^necoc/', include('necoc.foo.urls')),

    url(r'^api-token-auth/', ObtainAPIToken.as_view()),
    url(r'^api/v1/rapid-pro/$', RapidProListCreateView.as_view()),
    url(r'^login/$', Login.as_view(), name='login_page'),
    url(r'^logout/$', Logout.as_view(), name='login_page'),
    url(r'^api/v1/poll-responses/$', PollResponseListCreateView.as_view()),
    url(r'^api/v1/rapid-pro/(?P<id>[0-9a-z]+)/$', RapidProRetrieveUpdateView.as_view()),
    url(r'^api/v1/locations/$', LocationListCreateView.as_view()),
    url(r'^api/v1/polls/$', PollListCreateView.as_view()),
    url(r'^api/v1/mobile-users/$', UserProfileListCreateView.as_view()),
    url(r'^api/v1/sent-messages/$', SentMessageListCreateView.as_view()),
    url(r'^api/v1/disaster-types/$', DisasterTypeListCreateView.as_view()),
    url(r'^api/v1/disasters/$', DisasterListCreateView.as_view()),
    url(r'^api/v1/location-stats/$', LocationStatsListView.as_view()),
    url(r'^api/v1/location-stats/(?P<district>[0-9a-z]+)/$', DistrictStatsListView.as_view()),
    url(r'^export/poll-responses/(?P<poll_id>[0-9a-z]+)/$',
        login_required(ExportPollResponsesView.as_view(), login_url='login/')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

