from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


def check_existing_email(value):
    emails = User.objects.filter(email=value)
    if emails:
        raise ValidationError(
            'Email is already in the system and it belongs to %(username)s',
            params={'username': emails[0].username}
        )


def check_existing_user(value):
    users = User.objects.filter(username=value)
    if users:
        raise ValidationError('Username already exists')


class InvitationForm(forms.Form):
    username = forms.CharField(
        help_text='Please provide a good username',
        validators=[check_existing_user]
    )
    email = forms.EmailField(
        validators=[check_existing_email]
    )


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        # import ipdb; ipdb.set_trace()
        # self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=commit)
        user.is_active = True
        invite = user.invitation_set.last()
        invite.valid_until = timezone.now()
        if commit:
            user.save()
            invite.save()
        return user
