from django.contrib import admin
from tendenci.apps.api.models import DaJiDianYu
from tendenci.apps.api.forms import DaJiDianYuForm



class DaJiDianYuAdmin(admin.ModelAdmin):
    list_display = ['pk','form','form_name','serial_number','entry']
    model = DaJiDianYu
    form = DaJiDianYuForm

admin.site.register(DaJiDianYu, DaJiDianYuAdmin)
