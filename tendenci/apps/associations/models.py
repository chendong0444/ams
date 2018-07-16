from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import uuid


class Association(models.Model):
    name = models.CharField(max_length=255)
    guid = models.CharField(max_length=40)
    subdomain = models.CharField(max_length=255)
    owner = models.ForeignKey(User, null=True, default=None, on_delete=models.SET_NULL,
                              related_name="%(app_label)s_%(class)s_owner")
    wechat_mp_appid = models.CharField(max_length=255, null=True, blank=True)
    custom_domain = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = _("Associations")
        ordering = ('name',)
        app_label = 'associations'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.guid = str(uuid.uuid1())

        super(Association, self).save(*args, **kwargs)