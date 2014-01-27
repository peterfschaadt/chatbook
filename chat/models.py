from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from autoslug import AutoSlugField


class Chatroom(models.Model):
    name = models.CharField(max_length=50, blank=False)
    info = models.CharField(max_length=300, blank=False)
    slug = AutoSlugField(populate_from='name')
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='chatroom_creator', blank=False)
    # private = models.NullBooleanField()

    def get_absolute_url(self):
        return reverse('chatroom_view', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name


class ChatroomForm(ModelForm):
    """ Form to add Chatrooms """
    
    class Meta:
        model = Chatroom
        # Fields to include
        fields = ['name', 'info']


class Message(models.Model):
    text = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='message_creator', blank=False)
    chatroom = models.ForeignKey(Chatroom)

    def get_absolute_url(self):
        return reverse('message_view', kwargs={'slug': self.slug, 'pk': self.pk})

    # def __unicode__(self):
    #     return unicode(self.User + ': ' + self.text)

    class Meta:
        # Optional User permission to be able to delete Messages
        ('can_delete_messages', 'can delete messages'),


class MessageForm(ModelForm):
    """ Form to add Messages to Chatrooms """
    
    class Meta:
        model = Message
        # Fields to include
        fields = ['text']
