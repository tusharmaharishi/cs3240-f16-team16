from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'), #views.post_list is the place to go if we arrive at the main page
]

