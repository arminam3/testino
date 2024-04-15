from django import forms

from .models import Notification

class NotificationCreateForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('sender', 'receptor', 'title')
