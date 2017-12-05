import hashlib
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import FormView, UpdateView

from isi_mip.invitation.forms import InvitationForm, RegistrationForm
from isi_mip.invitation.models import Invitation


class InvitationView(FormView):
    template_name = 'invitation/invitation_form.html'
    form_class = InvitationForm
    email_subject_template = 'invitation/email_subject.txt'
    email_body_template = 'invitation/email_body.txt'

    def __init__(self, **kwargs):
        self.valid_until = timezone.now() + timezone.timedelta(days=getattr(settings, "INVITATION_VALID_DAYS", 7))
        super(InvitationView, self).__init__(**kwargs)

    def get_success_url(self):
        return reverse('climatemodels:assign', kwargs={'username': self.invite.user.username})+'?next='+\
               reverse('admin:auth_user_changelist')

    def form_valid(self, form):
        user = User.objects.create(
            username=form.data['username'],
            email=form.data['email'],
            is_active=True)
        self.invite = Invitation.objects.create(
            user=user,
            token=hashlib.sha1(os.urandom(128)).hexdigest(),
            valid_from=timezone.now(),
            valid_until=self.valid_until)

        messages.success(self.request, 'User has been created successfully.')
        return super(InvitationView, self).form_valid(form)


class RegistrationView(UpdateView):
    template_name = 'invitation/registration_form.html'
    form_class = RegistrationForm
    model = User

    success_url = '/dashboard/'
    error_url = '/'

    def dispatch(self, request, *args, **kwargs):
        pk, token = kwargs['pk'], kwargs['token']
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            messages.error(request, 'Invalid username')
            return HttpResponseRedirect(self.error_url)
        if user.is_active:
            messages.error(request, 'User is already activated')
            return HttpResponseRedirect(self.error_url)
        try:
            invite = Invitation.objects.get(user_id=pk, token=token)
        except:
            messages.error(request, 'No invite')
            return HttpResponseRedirect(self.error_url)
        if invite.valid_until < timezone.now():
            messages.error(request, 'Invite not valid anymore')
            return HttpResponseRedirect(self.error_url)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super(RegistrationView, self).form_valid(form)
        form.instance.backend = 'django.contrib.auth.backends.ModelBackend' # TODO: Replace this with "authenticate()"
        login(self.request, form.instance)
        return response