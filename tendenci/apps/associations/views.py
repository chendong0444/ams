from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from tendenci.apps.associations.forms import AssociationForm, AssociationJoinForm, AssociationChangeForm
from tendenci.apps.associations.models import Association


@login_required
def add(request, form_class=AssociationForm, template_name="associations/add.html"):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            asso = form.save()

            msg_string = 'Successfully added %s' % unicode(asso)
            messages.add_message(request, messages.SUCCESS, _(msg_string))

            # TODO: init association data(navs,boxes,stories,......)

            return HttpResponseRedirect(reverse('home'))
    else:
        form = form_class(user=request.user)

    return render_to_response(template_name, {'form': form},
                              context_instance=RequestContext(request))


@login_required
def join(request, form_class=AssociationJoinForm, template_name="associations/join.html"):
    if request.method == "POST":
        selected_association = request.POST['associations']
        if selected_association:
            association=Association.objects.get(id=selected_association)
            request.user.profile.associations.add(association)

            request.user.profile.current_association = association
            request.user.profile.save()

        return HttpResponseRedirect(reverse('home'))
    else:
        form = form_class(user=request.user)

    return render_to_response(template_name, {'form': form},
                              context_instance=RequestContext(request))


@login_required
def change(request, form_class=AssociationChangeForm, template_name="associations/change.html"):
    if request.method == "POST":
        association_id = request.POST['associations']
        if association_id:
            request.user.profile.current_association_id = association_id
            request.user.profile.save()

        return HttpResponseRedirect(reverse('home'))
    else:
        form = form_class(user=request.user)

    return render_to_response(template_name, {'form': form},
                              context_instance=RequestContext(request))