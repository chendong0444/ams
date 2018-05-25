from django import forms
from django.forms import fields
from .models import DaJiDianYu
from .widgets import JSONEditorWidget

class DaJiDianYuForm(forms.ModelForm):
    entry = forms.CharField(widget=JSONEditorWidget(attrs={'style': ''}))
    class Meta:
        model = DaJiDianYu
        fields = '__all__'
        widgets = {
            'entry': JSONEditorWidget()
        }
        # css = { 'all': ('jsoneditor/dist/jsoneditor.min.css',) }
        # js = ('https://warfares.github.io/pretty-json/pretty-json-min.js', )