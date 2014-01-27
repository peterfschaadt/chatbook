from django import forms
from .models import Chatroom, Message


class ChatroomForm(forms.ModelForm):
    
    class Meta:
        model = Chatroom
        field = ('name', 'info')
        # exclude = ('slug', 'created', 'created_by')

    def __init__(self, user, *args, **kwargs):
        super(ChatroomForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(ChatroomForm, self).save(*args, **kwargs)
        if self.request:
            obj.user = self.request.user
            obj.save()
        return obj


class MessageForm(forms.ModelForm):
    
    class Meta:
        model = Message
        field = ('text')

    def __init__(self, user, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(MessageForm, self).save(*args, **kwargs)
        if self.request:
            obj.user = self.request.user
            obj.save()
        return obj
