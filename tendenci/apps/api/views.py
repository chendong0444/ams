#coding=utf-8
import logging
from django.http import HttpResponse
import simplejson
from django.views.decorators.csrf import csrf_exempt
from tendenci.apps.api.utils import validate_api_request
from tendenci.apps.api.models import DaJiDianYu

handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)


logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

@csrf_exempt
def api_rp(request):
    """A Recurring Payment api.
       Supported functions: api_add_rp,
                            api_get_rp_token

    Result code:
        1001 - successful
        E004 - invalid request
        E005 - system error

    Test command:
    curl --dump-header - -H "Content-Type: application/json" -X POST
    --data '{"api_method": "api_add_rp", "email": "jqian@ams365.cn",
    "description": "self signup", "payment_amount": "20",
    "access_id":"jennytest", "time_stamp":"1317505435.040309",
    "h_sequence":"3b0b9655af8698d3d1b87ea913da3a41"}'
    http://127.0.0.1:8000/api/rp/

    curl --dump-header - -H "Content-Type: application/json" -X POST
    --data '{"api_method": "api_get_rp_token", "rp_id": "4",
    "access_id":"jennytest", "time_stamp":"1317505435.040309",
    "h_sequence":"3b0b9655af8698d3d1b87ea913da3a41"}'
    http://127.0.0.1:8000/api/rp/
    """
    result_code_success = {'result_code': '1001'}
    result_code_invalid = {'result_code': 'E004'}
    result_code_error = {'result_code': 'E005'}

    try:
        data = simplejson.loads(request.raw_post_data)
    except simplejson.JSONDecodeError:
        data = ''

    if not isinstance(data, dict):
        return  HttpResponse('')

    # SECURITY CHECK - access_id, secret_key(not passed), h_sequence
    is_valid = validate_api_request(data)
    if not is_valid:
        return HttpResponse('')

    method = data.get('api_method', '')
    if method == 'api_rp_setup':
        from tendenci.apps.recurring_payments.utils import api_rp_setup
        success, ret_data = api_rp_setup(data)
    else:
        return  HttpResponse('')

#    if method == 'api_add_rp':
#        from tendenci.apps.recurring_payments.utils import api_add_rp
#        success, ret_data = api_add_rp(data)
#    elif method == 'api_get_rp_token':
#        from tendenci.apps.recurring_payments.utils import api_get_rp_token
#        success, ret_data = api_get_rp_token(data)
#    elif method == 'api_verify_rp_payment_profile':
#        from tendenci.apps.recurring_payments.utils import api_verify_rp_payment_profile
#        success, ret_data = api_verify_rp_payment_profile(data)
#    else:
#        return  HttpResponse('')

    if success:
        ret_data.update(result_code_success)
    else:
        ret_data.update(result_code_invalid)

    return HttpResponse(simplejson.dumps(ret_data), content_type='application/json')

@csrf_exempt
def api_dajidianyu(request):
    '''
    接收昆山打击电鱼举报专线的数据（JSON格式）
    https://jinshuju.net/forms/uM6RFA/after_submission(登录账户找管理员)
    金数据将在收到数据后，向对应的HTTP地址 POST发送JSON格式数据。
    需在2秒内返回2XX（200，201等）作为应答。如果出错，金数据会重试最多六次。

    字段对照表及JSON样例:

    字段名称	数据类型	API Code
    序号	Float	serial_number
    现场取证图	Array	field_2
    作案地点	Hash	field_4
    您的手机号(保密）	String	field_3
    微信昵称	String	x_field_weixin_nickname
    微信性别	String	x_field_weixin_gender
    微信国家	String	x_field_weixin_country
    微信省市	Hash	x_field_weixin_province_city
    微信OpenID	String	x_field_weixin_openid
    微信头像	String	x_field_weixin_headimgurl
    提交人	String	creator_name
    提交时间	DateTime	created_at
    修改时间	DateTime	updated_at
    IP	String	info_remote_ip
    {
      "form": "uM6RFA",
      "form_name": "昆山打击电鱼举报专线",
      "entry": {
        "serial_number": 123,
        "field_2": [
          "https://example.jinshuju.net/en/key1?token=token&download",
          "https://example.jinshuju.net/en/key2?token=token&download"
        ],
        "field_4": {
          "longitude": 108.8725926,
          "latitude": 34.1927644,
          "address": "陕西省西安市锦业一路"
        },
        "field_3": "13812345678",
        "x_field_weixin_nickname": "小王",
        "x_field_weixin_gender": "男",
        "x_field_weixin_country": "中国",
        "x_field_weixin_province_city": {
          "province": "陕西",
          "city": "西安"
        },
        "x_field_weixin_openid": "adsfQWEasfxqw",
        "x_field_weixin_headimgurl": "http://wx.qlogo.cn/mmopen/m8kRxejzzH0/0",
        "creator_name": "小王",
        "created_at": "2018-05-24 02:04:17 UTC",
        "updated_at": "2018-05-24 02:04:17 UTC",
        "info_remote_ip": "127.0.0.1"
      }
    }
    :param request（json）:
    :return:
    '''
    result_code = 202

    if request.method == 'POST':
        try:
            logger.info(request.body)
            data = simplejson.loads(request.body)
        except simplejson.JSONDecodeError:
            data = ''

        if not isinstance(data, dict):
            return HttpResponse('')

        # SECURITY CHECK - access_id, secret_key(not passed), h_sequence
        # is_valid = validate_api_request(data)
        # if not is_valid:
        #     return HttpResponse('')

        d = DaJiDianYu()
        d.form = data.get('form', '')
        d.form_name = data.get('form_name', '')
        d.entry = data.get('entry', '')
        if d.entry:
            d.serial_number = float(d.entry.get('serial_number', ''))
        if d.serial_number:
            e = DaJiDianYu.objects.filter(serial_number=d.serial_number, form=d.form)
            if len(e) > 0:
                result_code = 201
            else:
                # print(d.entry)
                d.save()
                result_code = 200

    return HttpResponse(result_code, content_type='application/text')


@csrf_exempt
def api_open_weixin_callbak(request, appid):
    # https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1419318482&token=&lang=zh_CN
    EncodingAESKey = 'f0fba8d4165ecf6241f61e52381ec7c2Ylzjfww8989'
    # AESKey = Base64_Decode(EncodingAESKey + “=”)
    result_code = 200
    logger.info(request.get('signature', 'signature'))
    logger.info(request.get('timestamp', 'timestamp'))
    logger.info(request.get('nonce', 'nonce'))
    logger.info(request.get('encrypt_type', 'encrypt_type'))
    logger.info(request.get('msg_signature', 'msg_signature'))
    logger.info(appid)
    logger.info(request.body)

    return HttpResponse(result_code, content_type='application/text')
