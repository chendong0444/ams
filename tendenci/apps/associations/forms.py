from form_utils.forms import BetterForm

from tendenci.apps.associations.models import Association
from django.utils.translation import ugettext_lazy as _
from django import forms

from tendenci.apps.base.forms import FormControlWidgetMixin
from tendenci.apps.profiles.models import Profile


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


class AssociationJoinForm(forms.ModelForm):
    associations = forms.ModelChoiceField(label=_('Select Association'), queryset=Association.objects.none())

    class Meta:
        model = Profile
        fields = ('associations',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AssociationJoinForm, self).__init__(*args, **kwargs)
        if self.user:
            profile_associations = self.user.profile.associations.values_list('pk', flat=True)
            non_associations = Association.objects.exclude(pk__in=profile_associations)
            self.fields['associations'].queryset = non_associations


class AssociationChangeForm(forms.ModelForm):
    associations = forms.ModelChoiceField(label=_('Select Association'), queryset=Association.objects.none())

    class Meta:
        model = Profile
        fields = ('associations',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AssociationChangeForm, self).__init__(*args, **kwargs)
        if self.user:
            profile_associations = self.user.profile.associations.all()
            self.fields['associations'].queryset = profile_associations
