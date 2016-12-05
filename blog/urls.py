from django.conf.urls import include, url
from . import views

urlpatterns = [
#    url(r'^$', views.login, name='login'),
    url(r'^$', views.report_list, name='report_list'), #views.report_list is the place to go if we arrive at the main page
    url(r'^report/(?P<pk>\d+)/$', views.report_detail, name='report_detail'),
    url(r'^report/new/$', views.report_new, name='report_new'),
    url(r'^report/(?P<pk>\d+)/edit/$', views.report_edit, name='report_edit'),
    url(r'^drafts/$', views.report_draft_list, name='report_draft_list'),
    url(r'^report/(?P<pk>\d+)/publish/$', views.report_publish, name='report_publish'),
    url(r'^report/(?P<pk>\d+)/remove/$', views.report_remove, name='report_remove'),
#    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^group/$', views.group_list, name='group_list'),
    url(r'^group/new/$', views.group_new, name='group_new'),
    url(r'^group/(?P<pk>\d+)/$', views.group_detail, name='group_detail'),
    url(r'^group/(?P<pk>\d+)/adduser$', views.group_adduser, name='group_adduser'),
    url(r'^group/(?P<pk>\d+)/removeuser&', views.group_removeuser, name='group_removeuser'),
    url(r'^folder/new/$', views.folder_new, name='folder_new'),
    url(r'^folder/$', views.folder_list, name='folder_list'),
    url(r'^folder/(?P<pk>\d+)/remove/$', views.folder_remove, name='folder_remove'),
    url(r'^folder/(?P<pk>\d+)/edit/$', views.folder_edit, name='folder_edit'),
    url(r'^folder/(?P<pk>\d+)/$', views.folder_detail, name='folder_detail'),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^get_unread_messages', views.get_unread_messages)
    #url(r'^group/(?P<pk>\d+)/add/$', views.add_user, name='add_user'),

    #comment out if not working:
    #url(r'^search/$', search_file),
]

