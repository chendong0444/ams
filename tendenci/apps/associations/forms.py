from form_utils.forms import BetterForm

from tendenci.apps.associations.models import Association
from django.utils.translation import ugettext_lazy as _
from django import forms

from tendenci.apps.base.forms import FormControlWidgetMixin


class AssociationForm(forms.ModelForm):
    name = forms.CharField(required=True, label=_('Name'))
    # guid = forms.CharField(label=_('GUID'))
    subdomain = forms.CharField(label=_('SubDomain'))

    class Meta:
        model = Association
        fields = ('name', 'subdomain')

    def save(self, *args, **kwargs):
        asso = super(AssociationForm, self).save(*args, **kwargs)
        return asso

    def __init__(self, *args, **kwargs):
        super(AssociationForm, self).__init__(*args, **kwargs)
