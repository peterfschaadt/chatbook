from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from chat import views
from django.contrib import admin
admin.autodiscover()
import settings


# import chat.urls

urlpatterns = patterns('',

    # urls specific to this app
    # url(r'^chat/', include(chat.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # User accounts
    url(r'^accounts/', include('django.contrib.auth.urls')),
    # url(r'^accounts/', include('registration.urls')),

    # User profiles
    url(r'^accounts/profile/$', 
    	views.UserProfile.as_view(), name='user_profile'),

    # catch all, redirect to chat home view
    # url(r'.*', RedirectView.as_view(url='/chat/home')),

    url(r'^home/$', 
    	views.Home.as_view(), name='home'),

    url(r'^chatrooms/$', 
    	views.ChatroomList.as_view(), name='chatroom_list'),

    url(r'^chatrooms/create/$', 
    	views.ChatroomCreate.as_view(), name='chatroom_create_form'),

    url(r'^chatrooms/(?P<slug>[-\w]+)/$', 
    	views.ChatroomView.as_view(), name='chatroom'),

    url(r'^chatrooms/(?P<slug>[-\w]+)/create/$',
    	views.MessageCreate.as_view(), name='message_create_form'),

    url(r'^chatrooms/(?P<slug>[-\w]+)/(?P<message_pk>\d+)/$',
    	views.MessageView.as_view(), name='message_view'),

    ### For deleting Chatrooms and Messages

    # url(r'^chatrooms/delete/$', 
    # 	views.ChatroomDelete.as_view(), name='chatroom_delete_form'),

    # url(r'^chatrooms/(?P<chatroom_slug>[-\w]+)/(?P<message_pk>\d+)/delete/$',
   	#   views.MessageDelete.as_view(), name='message_delete_form'),

)
