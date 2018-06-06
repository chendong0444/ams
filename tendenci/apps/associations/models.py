from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid


class Association(models.Model):
    name = models.CharField(max_length=255)
    guid = models.CharField(max_length=40)
    subdomain = models.CharField(max_length=255)


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