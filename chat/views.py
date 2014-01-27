from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin
from .models import Chatroom, Message
from .forms import ChatroomForm, MessageForm


class Home(ListView):
    """ View for Home page with recent Chatrooms """
    context_object_name = 'chatroom'
    model = Chatroom
    template_name = 'chat/home.html'

    def get_queryset(self):
        # Display 5 most recent chatrooms
        filters = {}
        return Chatroom.objects.order_by('-created').filter(**filters)[:5]

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['recent_chatrooms'] = self.get_queryset()
        return context


class ChatroomList(ListView):
    """ View of available chatrooms """
    context_object_name = 'chatroom'
    template_name = 'chat/chatroom_list.html'

    def get_queryset(self):
        # Order all chatrooms by creation time
        all_chatrooms = Chatroom.objects.order_by('-created')
        return all_chatrooms

    def get_context_data(self, **kwargs):
        context = super(ChatroomList, self).get_context_data(**kwargs)
        context['all_chatrooms'] = self.get_queryset()
        return context


class ChatroomCreate(LoginRequiredMixin, CreateView):
    """ View to create a new Chatroom """
    model = Chatroom
    # form_class = ChatroomForm
    # Fields for creating a chatroom
    fields = ['name', 'info']
    success_url = '/chatrooms/%(slug)s/'

    def form_valid(self, form):
        object = form.save(commit=False)
        # Save request User as creator of Chatroom
        object.created_by = self.request.user
        object.save()
        return super(ChatroomCreate, self).form_valid(form)


class ChatroomView(DetailView):
    """ View of Messages in individual Chatroom """
    model = Chatroom
    context_object_name = 'recent_messages'
    context_object_name = 'chatroom'
    template_name = 'chat/chatroom.html'
    # Slug
    slug_url_kwarg = 'slug'
    # slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ChatroomView, self).get_context_data(**kwargs)
        context['chatroom'] = self.object
        # Display 50 most recent Messages in Chatroom
        context['recent_messages'] = Message.objects.filter(chatroom=self.object)[:50]
        return context


class MessageCreate(LoginRequiredMixin, CreateView):
    """ View to create a new Message and add to Chatroom """
    # Requires JSONResponseMixin and AjaxResponseMixin for AJAX
    model = Message
    fields = ['text']
    # success_url = '/chatrooms/%(slug)s/%(pk)d'
    success_url = '/chatrooms/'

    def get_context_data(self, **kwargs):
        context = super(MessageCreate, self).get_context_data(**kwargs)
        # context['chatroom_slug'] = Chatroom.objects.get(slug=self.kwargs['slug'])
        context['slug'] = self.kwargs['slug']
        return context

    def form_valid(self, form):
        # Add slug to Form, then save to Model
        object = form.save(commit=False)
        object.created_by = self.request.user

        # Grab Chatroom by its slug
        message_chatroom_slug = self.kwargs['slug']
        object.chatroom = Chatroom.objects.get(slug=message_chatroom_slug)

        # Save Form to Model (commit=True)
        object.save()
        return super(MessageCreate, self).form_valid(form)

    # def post_ajax(self, request, *args, **kwargs):
    #     """ This method allows us to POST messages via jQuery with AJAX """
    #     super(MessageCreate, self).post(request, *args, **kwargs)
    #     return self.render_json_response({'status': 'success'})


class MessageView(LoginRequiredMixin, DetailView):
    """ View to display a Message """
    model = Message
    context_object_name = 'message'
    template_name = 'chat/message.html'


class UserProfile(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'message'
    template_name = 'chat/user_profile.html'

    def get_queryset(self):
        # Return 25 recent Messages sorted by creation time
        recent_messages = Message.objects.filter(created_by=self.request.user).order_by('-created')[:25]
        return recent_messages

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['recent_messages'] = self.get_queryset()
        return context
