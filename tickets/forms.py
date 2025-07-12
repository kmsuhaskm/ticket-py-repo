from django import forms
from .models import Ticket, TicketReply
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'attachment']

class TicketReplyForm(forms.ModelForm):
    class Meta:
        model = TicketReply
        fields = ['message']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
