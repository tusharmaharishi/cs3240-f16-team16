from django.conf.urls import include, url
from . import views

urlpatterns = [
#    url(r'^$', views.login, name='login'),
    url(r'^$', views.post_list, name='post_list'), #views.post_list is the place to go if we arrive at the main page
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
#    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^group/$', views.group_list, name='group_list'),
    url(r'^group/new/$', views.group_new, name='group_new'),
    url(r'^group/(?P<pk>\d+)/$', views.group_detail, name='group_detail'),
    url(r'^group/(?P<pk>\d+)/adduser$', views.group_adduser, name='group_adduser'),
    url(r'^folder/new/$', views.folder_new, name='folder_new'),
    url(r'^folder/$', views.folder_list, name='folder_list'),
    url(r'^folder/(?P<pk>\d+)/$', views.folder_detail, name='folder_detail'),
    #url(r'^group/(?P<pk>\d+)/add/$', views.add_user, name='add_user'),
]

