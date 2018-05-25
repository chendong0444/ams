#coding=utf-8
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
import simplejson


class JSONEditorWidget(forms.Widget):
    template_name = 'jsoneditor.html'

    def render(self, name, value, attrs=None):
        # print(value)
        # value = simplejson.dumps(value, ensure_ascii=False, encoding='utf-8')
        if value:
            value = value.replace('"', '').replace("u'", "'")
        # print(value)
#         value = '''
#             {
#   "form": "uM6RFA",
#   "form_name": "昆山打击电鱼举报专线",
#   "entry": {
#     "serial_number": 123,
#     "field_2": [
#       "https://example.jinshuju.net/en/key1?token=token&download",
#       "https://example.jinshuju.net/en/key2?token=token&download"
#     ],
#     "field_4": {
#       "longitude": 108.8725926,
#       "latitude": 34.1927644,
#       "address": "陕西省西安市锦业一路"
#     },
#     "field_3": "13812345678",
#     "x_field_weixin_nickname": "小王",
#     "x_field_weixin_gender": "男",
#     "x_field_weixin_country": "中国",
#     "x_field_weixin_province_city": {
#       "province": "陕西",
#       "city": "西安"
#     },
#     "x_field_weixin_openid": "adsfQWEasfxqw",
#     "x_field_weixin_headimgurl": "http://wx.qlogo.cn/mmopen/m8kRxejzzH0/0",
#     "creator_name": "小王",
#     "created_at": "2018-05-25 01:11:40 UTC",
#     "updated_at": "2018-05-25 01:11:40 UTC",
#     "info_remote_ip": "127.0.0.1"
#   }
# }
#             '''
        context = {
            'entry': value,
            'name': name
        }

        return mark_safe(render_to_string(self.template_name, context))