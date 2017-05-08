from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from isi_mip.climatemodels.models import Sector, BaseImpactModel, ImpactModel


class Role(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)


class Country(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institute = models.CharField(max_length=500, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    sector = models.ManyToManyField(Sector, blank=True, related_name='user_sectors')
    comment = models.TextField(blank=True, null=True)
    owner = models.ManyToManyField(BaseImpactModel, blank=True, related_name='impact_model_owner')
    involved = models.ManyToManyField(ImpactModel, blank=True, related_name='impact_model_involved')

    @property
    def name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return "%s (%s) - %s" % (self.name, self.institute, self.email)

    def pretty(self):
        return "{0.name} (<a href='mailto:{0.email}'>{0.email}</a>), {0.institute}{1}".format(self, self.country and " (%s)" % self.country.name or '')

    class Meta:
        ordering = ('user__last_name',)


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=User)
