from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib.auth.decorators import login_required
from dms.api.admin_setting_endpoint import AdminSettingListCreateView, AdminSettingUpdateView
from dms.api.bulk_sms_endpoint import SentMessageListCreateView
from dms.api.current_permissions_endpoint import CurrentPermissionsView
from dms.api.disaster_endpoint import DisasterListCreateView, DisasterView, CSVDisasterView
from dms.api.disaster_type_endpoint import DisasterTypeListCreateView
from dms.api.groups_endpoint import GroupsEndpointListView
from dms.api.location_stats_service_endpoint import LocationStatsListView, DistrictStatsListView
from dms.api.password_change_endpoint import PasswordChangeView, PasswordResetView
from dms.api.poll_endpoint import PollListCreateView
from dms.api.poll_response_endpoint import PollResponseListCreateView, CSVPollResponsesView
from dms.api.rapid_pro_endpoint import RapidProListCreateView, RapidProRetrieveUpdateView, CSVMessageView
from dms.api.location_endpoint import LocationListCreateView
from dms.api.response_message_endpoint import ResponseMessageListCreateView
from dms.api.stats_summary_service_endpoint import SummaryStatsListView
from dms.api.user_profile_endpoint import UserProfileListCreateView, UserProfileView, CSVUserProfileView, \
    BulkUserProfileView
from dms.views.api_token import ObtainAPIToken
from dms.views.export_poll_responses import ExportPollResponsesView
from dms.views.homepage import HomeView
from dms.views.login import Login, Logout
from dms.views.profile_image import ProfileImageView


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
    url(r'^api/v1/photo/(?P<id>[0-9a-z]+)/$', ProfileImageView.as_view()),
    url(r'^api/v1/locations/$', LocationListCreateView.as_view()),
    url(r'^api/v1/polls/$', PollListCreateView.as_view()),
    url(r'^api/v1/groups/$', GroupsEndpointListView.as_view()),
    url(r'^api/v1/mobile-users/$', UserProfileListCreateView.as_view()),
    url(r'^api/v1/mobile-users/(?P<id>[0-9a-z]+)/$', UserProfileView.as_view()),
    url(r'^api/v1/mobile-users/(?P<ordering>[\-0-9a-z]+)/$', UserProfileView.as_view()),
    url(r'^api/v1/mobile-users/(?P<id>[0-9a-z]+)/password/$', PasswordChangeView.as_view()),
    url(r'^api/v1/mobile-users/(?P<id>[0-9a-z]+)/password_reset/$', PasswordResetView.as_view()),
    url(r'^api/v1/sent-messages/$', SentMessageListCreateView.as_view()),
    url(r'^api/v1/response-messages/$', ResponseMessageListCreateView.as_view()),
    url(r'^api/v1/response-messages/(?P<step>[\-0-9a-zA-Z_]+)/$', ResponseMessageListCreateView.as_view()),
    url(r'^api/v1/disaster-types/$', DisasterTypeListCreateView.as_view()),
    url(r'^api/v1/disasters/$', DisasterListCreateView.as_view()),
    url(r'^api/v1/disasters/(?P<id>[0-9a-z]+)/$', DisasterView.as_view()),
    url(r'^api/v1/current-permissions/$', CurrentPermissionsView.as_view()),
    url(r'^api/v1/stats-summary/$', SummaryStatsListView.as_view()),
    url(r'^api/v1/location-stats/$', LocationStatsListView.as_view()),
    url(r'^api/v1/location-stats/(?P<district>[0-9a-z]+)/$', DistrictStatsListView.as_view()),
    url(r'^api/v1/admin-settings/$', AdminSettingListCreateView.as_view()),
    url(r'^api/v1/admin-settings/(?P<name>[0-9a-zA-Z_]+)/$', AdminSettingUpdateView.as_view()),
    url(r'^api/v1/csv-messages/$', CSVMessageView.as_view()),
    url(r'^api/v1/csv-poll/$', CSVPollResponsesView.as_view()),
    url(r'^api/v1/csv-mobile-users/$', CSVUserProfileView.as_view()),
    url(r'^api/v1/bulk-mobile-users/$', BulkUserProfileView.as_view()),
    url(r'^api/v1/csv-disasters/$', CSVDisasterView.as_view()),
    # url(r'^api/v1/csvm/$', CSVMView.as_view()),
    url(r'^export/poll-responses/(?P<poll_id>[0-9a-z]+)/$',
        login_required(ExportPollResponsesView.as_view(), login_url='login/')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

