from datetime import datetime, timedelta
import subprocess, time
import string
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template.defaultfilters import slugify
import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from tendenci.libs.utils import python_executable
from tendenci.apps.site_settings.utils import get_setting
from tendenci.apps.base.decorators import password_required
from tendenci.apps.base.http import Http403
from tendenci.apps.base.views import file_display
from tendenci.apps.perms.decorators import is_enabled
from tendenci.apps.perms.utils import (get_notice_recipients,
    has_perm, has_view_perm, get_query_filters, update_perms_and_save)
from tendenci.apps.event_logs.models import EventLog
from tendenci.apps.meta.models import Meta as MetaTags
from tendenci.apps.meta.forms import MetaForm
from tendenci.apps.theme.shortcuts import themed_response as render_to_response

from tendenci.apps.directories.models import Directory, DirectoryPricing
from tendenci.apps.directories.models import Category as DirectoryCategory
from tendenci.apps.directories.forms import (DirectoryForm, DirectoryPricingForm,
                                               DirectoryRenewForm, DirectoryExportForm)
from tendenci.apps.directories.utils import directory_set_inv_payment, is_free_listing
from tendenci.apps.notifications import models as notification
from tendenci.apps.base.utils import send_email_notification
from tendenci.apps.directories.forms import DirectorySearchForm


@login_required
def add(request):  #, form_class=DirectoryForm, template_name="directories/add.html"):
    pass
