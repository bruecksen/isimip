from django.db import models
from django.contrib.auth.models import User

from isi_mip.climatemodels.models import Sector, BaseImpactModel


class Role(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institute = models.CharField(max_length=500, null=True, blank=True)
    sector = models.ManyToManyField(Sector, blank=True, related_name='user_sectors')
    role = models.ManyToManyField(Role, blank=True, related_name='user_roles')
    comment = models.TextField(blank=True, null=True)
    owner = models.ManyToManyField(BaseImpactModel, blank=True, related_name='impact_model_owner')
    involved = models.ManyToManyField(BaseImpactModel, blank=True, related_name='impact_model_involved')

    @property
    def name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return "%s (%s) - %s" % (self.name, self.institute, self.email)

    def pretty(self):
        return "{0.name} (<a href='mailto:{0.email}'>{0.email}</a>), {0.institute}".format(self)

    class Meta:
        ordering = ('user__last_name',)
