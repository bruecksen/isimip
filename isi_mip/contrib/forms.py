from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UsernameField)


class AuthenticationForm(AuthenticationForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': ''}),
        label='Username or email'
    )
