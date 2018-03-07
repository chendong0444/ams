# -*- coding:utf-8 -*-

from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from tendenci.apps.payments.forms import PaymentSearchForm
from tendenci.apps.payments.models import Payment
from tendenci.apps.payments.authorizenet.utils import prepare_authorizenet_sim_form
from tendenci.apps.invoices.models import Invoice
from tendenci.apps.base.http import Http403
from tendenci.apps.event_logs.models import EventLog

from tendenci.apps.site_settings.utils import get_setting
from wxpay_sdk import PayNotifyCallBack, WxPayBasic
import xmltodict
import logging

# 通过下面的方式进行简单配置输出方式与日志级别
logging.basicConfig(filename='logger.log', level=logging.INFO)


def pay_online2(request, invoice_id, guid="", template_name="payments/pay_online.html"):
    print('pay_online')


def pay_online(request, invoice_id, guid="", template_name="payments/pay_online.html"):
    # check if they have the right to view the invoice
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if not invoice.allow_view_by(request.user, guid):
        raise Http403

    # tender the invoice
    if not invoice.is_tendered:
        invoice.tender(request.user)
        # log an event for invoice edit
        EventLog.objects.log(instance=invoice)

    # generate the payment
    payment = Payment()

    boo = payment.payments_pop_by_invoice_user(request.user, invoice, guid)
    # log an event for payment add
    EventLog.objects.log(instance=payment)

    # post payment form to gateway and redirect to the vendor so customer can pay from there
    if boo:
        merchant_account = (get_setting("site", "global", "merchantaccount")).lower()

        if merchant_account == 'stripe':
            return HttpResponseRedirect(reverse('stripe.payonline', args=[payment.id]))
        elif merchant_account == "authorizenet":
            form = prepare_authorizenet_sim_form(request, payment)
            post_url = settings.AUTHNET_POST_URL
        elif merchant_account == 'firstdata':
            from tendenci.apps.payments.firstdata.utils import prepare_firstdata_form
            form = prepare_firstdata_form(request, payment)
            post_url = settings.FIRSTDATA_POST_URL
        elif merchant_account == 'firstdatae4':
            from tendenci.apps.payments.firstdatae4.utils import prepare_firstdatae4_form
            form = prepare_firstdatae4_form(request, payment)
            post_url = settings.FIRSTDATAE4_POST_URL
        elif merchant_account == 'paypalpayflowlink':
            from tendenci.apps.payments.payflowlink.utils import prepare_payflowlink_form
            form = prepare_payflowlink_form(request, payment)
            post_url = settings.PAYFLOWLINK_POST_URL
        elif merchant_account == 'paypal':
            from tendenci.apps.payments.paypal.utils import prepare_paypal_form
            form = prepare_paypal_form(request, payment)
            post_url = settings.PAYPAL_POST_URL
        elif merchant_account == 'wechat-pay':
            params = {

                'body': payment.description,  # 商品或支付单简要描述,例如：Ipad mini  16G  白色

                'out_trade_no': payment.guid.replace('-', ''),  # 商户系统内部的订单号,32个字符内、可包含字母

                'total_fee': int(payment.amount * 100),  # 订单总金额，单位为分

                'product_id': invoice_id,  # 商品ID

                'notify_url': 'https://www.kunshanfa.com/payments/wxcallback/',

                'trade_type': 'NATIVE',

            }
            wxpay = WxPayBasic(settings.WECHATPAY_CONFIG)
            code_url = wxpay.unifiedorder2_get_code_url(**params)
            print(code_url)
            template_name = 'payments/wechatpay.html'
            return render_to_response(template_name,
                                      {'code_url': code_url}, context_instance=RequestContext(request))
        else:   # more vendors
            form = None
            post_url = ""
    else:
        form = None
        post_url = ""
    return render_to_response(template_name,
        {'form': form, 'post_url': post_url
        }, context_instance=RequestContext(request))


def view(request, id, guid=None, template_name="payments/view.html"):
    payment = get_object_or_404(Payment, pk=id)

    if not payment.allow_view_by(request.user, guid):
        raise Http403

    return render_to_response(template_name, {'payment': payment},
        context_instance=RequestContext(request))


def receipt(request, id, guid, template_name='payments/receipt.html'):
    payment = get_object_or_404(Payment, pk=id)
    if payment.guid != guid:
        raise Http403

    return render_to_response(template_name, {'payment': payment},
                              context_instance=RequestContext(request))


@login_required
def search(request, template_name='payments/search.html'):
    search_criteria = None
    search_text = None
    search_method = None

    form = PaymentSearchForm(request.GET)
    if form.is_valid():
        search_criteria = form.cleaned_data.get('search_criteria')
        search_text = form.cleaned_data.get('search_text')
        search_method = form.cleaned_data.get('search_method')

    payments = Payment.objects.all()
    if search_criteria and search_text:
        search_type = '__iexact'
        if search_method == 'starts_with':
            search_type = '__istartswith'
        elif search_method == 'contains':
            search_type = '__icontains'
        search_filter = {'%s%s' % (search_criteria,
                                   search_type): search_text}
        payments = payments.filter(**search_filter)

    if request.user.profile.is_superuser:
        payments = payments.order_by('-create_dt')
    else:
        from django.db.models import Q
        payments = payments.filter(Q(creator=request.user) | Q(owner=request.user)).order_by('-create_dt')

    return render_to_response(template_name, {'payments': payments, 'form': form},
                              context_instance=RequestContext(request))


@csrf_exempt
def wxcallback(request, *args, **kwargs):
    req_xml_str = request.body
    logging.info(req_xml_str)
    return HttpResponse('<html>aaaa</br>%s</html>' % req_xml_str, content_type='text/html')


    wxpay = WxPayBasic(conf=settings.WECHATPAY_CONFIG)
    res_xml_str = wxpay.wxpay_callback(req_xml_str)
    logging.info(res_xml_str)

    res_xml_dict = xmltodict.parse(res_xml_str)
    logging.info(res_xml_dict)

    if res_xml_dict['xml']['return_code'] == 'SUCCESS':
        # 处理商户订单逻辑
        req_xml_dict = xmltodict.parse(req_xml_str)
        logging.info(req_xml_str)

        total_fee = req_xml_dict['xml']['total_fee']
        out_trade_no = req_xml_dict['xml']['out_trade_no']
    else:
        logging.info('wxpay callback error')

    return HttpResponse(res_xml_str, content_type='text/xml')

