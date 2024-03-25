
from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phoneNumber', 'message']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commenter_name', 'commenter_email', 'comment']
