#!/usr/bin/env python
#-*- encoding:utf-8 -*-

""" 对公众平台发送给公众账号的消息加解密示例代码.
@copyright: Copyright (c) 1998-2014 Tencent Inc.

"""
# ------------------------------------------------------------------------

import base64
import string
import random
import hashlib
import time
import requests
import struct
from Crypto.Cipher import AES
import xml.etree.cElementTree as ET
import sys
import logging
import socket
import re
import shutil
from django.core.cache import cache

reload(sys)
import ierror
sys.setdefaultencoding('utf-8')


handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)


logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

"""
关于Crypto.Cipher模块，ImportError: No module named 'Crypto'解决方案
请到官方网站 https://www.dlitz.net/software/pycrypto/ 下载pycrypto。
下载后，按照README中的“Installation”小节的提示进行pycrypto安装。
"""
class FormatException(Exception):
    pass

def throw_exception(message, exception_class=FormatException):
    """my define raise exception function"""
    raise exception_class(message)

class SHA1:
    """计算公众平台的消息签名接口"""

    def getSHA1(self, token, timestamp, nonce, encrypt):
        """用SHA1算法生成安全签名
        @param token:  票据
        @param timestamp: 时间戳
        @param encrypt: 密文
        @param nonce: 随机字符串
        @return: 安全签名
        """
        try:
            sortlist = [token, timestamp, nonce, encrypt]
            sortlist.sort()
            sha = hashlib.sha1()
            sha.update("".join(sortlist))
            return  ierror.WXBizMsgCrypt_OK, sha.hexdigest()
        except Exception,e:
            #print e
            return  ierror.WXBizMsgCrypt_ComputeSignature_Error, None


class XMLParse:
    """提供提取消息格式中的密文及生成回复消息格式的接口"""

    # xml消息模板
    AES_TEXT_RESPONSE_TEMPLATE = """<xml>
<Encrypt><![CDATA[%(msg_encrypt)s]]></Encrypt>
<MsgSignature><![CDATA[%(msg_signaturet)s]]></MsgSignature>
<TimeStamp>%(timestamp)s</TimeStamp>
<Nonce><![CDATA[%(nonce)s]]></Nonce>
</xml>"""

    # def extract(self, xmltext):
    #     """提取出xml数据包中的加密消息
    #     @param xmltext: 待提取的xml字符串
    #     @return: 提取出的加密消息字符串
    #     """
    #     try:
    #         xml_tree = ET.fromstring(xmltext)
    #         encrypt  = xml_tree.find("Encrypt")
    #         # touser_name    = xml_tree.find("ToUserName")
    #         return  ierror.WXBizMsgCrypt_OK, encrypt.text, touser_name.text
    #     except Exception,e:
    #         #print e
    #         return  ierror.WXBizMsgCrypt_ParseXml_Error,None,None

    def extract_node(self, xmltext, node):
        try:
            xml_tree = ET.fromstring(xmltext)
            encrypt = xml_tree.find(node)
            return ierror.WXBizMsgCrypt_OK, encrypt.text
        except Exception,e:
            print e
            return ierror.WXBizMsgCrypt_ParseXml_Error, None



    def generate(self, encrypt, signature, timestamp, nonce):
        """生成xml消息
        @param encrypt: 加密后的消息密文
        @param signature: 安全签名
        @param timestamp: 时间戳
        @param nonce: 随机字符串
        @return: 生成的xml字符串
        """
        resp_dict = {
                    'msg_encrypt' : encrypt,
                    'msg_signaturet': signature,
                    'timestamp'    : timestamp,
                    'nonce'        : nonce,
                     }
        resp_xml = self.AES_TEXT_RESPONSE_TEMPLATE % resp_dict
        return resp_xml


class PKCS7Encoder():
    """提供基于PKCS7算法的加解密接口"""

    block_size = 32
    def encode(self, text):
        """ 对需要加密的明文进行填充补位
        @param text: 需要进行填充补位操作的明文
        @return: 补齐明文字符串
        """
        text_length = len(text)
        # 计算需要填充的位数
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        # 获得补位所用的字符
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def decode(self, decrypted):
        """删除解密后明文的补位字符
        @param decrypted: 解密后的明文
        @return: 删除补位字符后的明文
        """
        pad = ord(decrypted[-1])
        if pad<1 or pad >32:
            pad = 0
        return decrypted[:-pad]


class Prpcrypt(object):
    """提供接收和推送给公众平台消息的加解密接口"""

    def __init__(self,key):
        #self.key = base64.b64decode(key+"=")
        self.key = key
        # 设置加解密模式为AES的CBC模式
        self.mode = AES.MODE_CBC


    def encrypt(self,text,appid):
        """对明文进行加密
        @param text: 需要加密的明文
        @return: 加密得到的字符串
        """
        # 16位随机字符串添加到明文开头
        text = self.get_random_str() + struct.pack("I",socket.htonl(len(text))) + text + appid
        # 使用自定义的填充方式对明文进行补位填充
        pkcs7 = PKCS7Encoder()
        text = pkcs7.encode(text)
        # 加密
        cryptor = AES.new(self.key,self.mode,self.key[:16])
        try:
            ciphertext = cryptor.encrypt(text)
            # 使用BASE64对加密后的字符串进行编码
            return ierror.WXBizMsgCrypt_OK, base64.b64encode(ciphertext)
        except Exception,e:
            #print e
            return  ierror.WXBizMsgCrypt_EncryptAES_Error,None

    def decrypt(self,text,appid):
        """对解密后的明文进行补位删除
        @param text: 密文
        @return: 删除填充补位后的明文
        """
        try:
            cryptor = AES.new(self.key,self.mode,self.key[:16])
            # 使用BASE64对密文进行解码，然后AES-CBC解密
            plain_text  = cryptor.decrypt(base64.b64decode(text))
        except Exception,e:
            #print e
            return  ierror.WXBizMsgCrypt_DecryptAES_Error,None
        try:
            pad = ord(plain_text[-1])
            # 去掉补位字符串
            #pkcs7 = PKCS7Encoder()
            #plain_text = pkcs7.encode(plain_text)
            # 去除16位随机字符串
            content = plain_text[16:-pad]
            xml_len = socket.ntohl(struct.unpack("I",content[ : 4])[0])
            xml_content = content[4 : xml_len+4]
            from_appid = content[xml_len+4:]
        except Exception,e:
            #print e
            return  ierror.WXBizMsgCrypt_IllegalBuffer,None
        if  from_appid != appid:
            return ierror.WXBizMsgCrypt_ValidateAppid_Error,None
        return 0,xml_content

    def get_random_str(self):
        """ 随机生成16位字符串
        @return: 16位字符串
        """
        rule = string.letters + string.digits
        str = random.sample(rule, 16)
        return "".join(str)

class WXBizMsgCrypt(object):
    #构造函数
    #@param sToken: 公众平台上，开发者设置的Token
    # @param sEncodingAESKey: 公众平台上，开发者设置的EncodingAESKey
    # @param sAppId: 企业号的AppId
    def __init__(self,sToken,sEncodingAESKey,sAppId):
        try:
            self.key = base64.b64decode(sEncodingAESKey+"=")
            assert len(self.key) == 32
        except:
            throw_exception("[error]: EncodingAESKey unvalid !", FormatException)
           #return ierror.WXBizMsgCrypt_IllegalAesKey)
        self.token = sToken
        self.appid = sAppId

    def EncryptMsg(self, sReplyMsg, sNonce, timestamp = None):
        #将公众号回复用户的消息加密打包
        #@param sReplyMsg: 企业号待回复用户的消息，xml格式的字符串
        #@param sTimeStamp: 时间戳，可以自己生成，也可以用URL参数的timestamp,如为None则自动用当前时间
        #@param sNonce: 随机串，可以自己生成，也可以用URL参数的nonce
        #sEncryptMsg: 加密后的可以直接回复用户的密文，包括msg_signature, timestamp, nonce, encrypt的xml格式的字符串,
        #return：成功0，sEncryptMsg,失败返回对应的错误码None
        pc = Prpcrypt(self.key)
        ret,encrypt = pc.encrypt(sReplyMsg, self.appid)
        if ret != 0:
            return ret,None
        if timestamp is None:
            timestamp = str(int(time.time()))
        # 生成安全签名
        sha1 = SHA1()
        ret,signature = sha1.getSHA1(self.token, timestamp, sNonce, encrypt)
        if ret != 0:
            return ret,None
        xmlParse = XMLParse()
        return ret,xmlParse.generate(encrypt, signature, timestamp, sNonce)

    def DecryptMsg(self, sPostData, sMsgSignature, sTimeStamp, sNonce, in_node, out_node):
        # 检验消息的真实性，并且获取解密后的明文
        # @param sMsgSignature: 签名串，对应URL参数的msg_signature
        # @param sTimeStamp: 时间戳，对应URL参数的timestamp
        # @param sNonce: 随机串，对应URL参数的nonce
        # @param sPostData: 密文，对应POST请求的数据
        #  xml_content: 解密后的原文，当return返回0时有效
        # @return: 成功0，失败返回对应的错误码
         # 验证安全签名
        xmlParse = XMLParse()
        # ret,encrypt,touser_name = xmlParse.extract(sPostData)
        ret, encrypt = xmlParse.extract_node(sPostData, in_node)
        if ret != 0:
            return ret, None
        sha1 = SHA1()
        ret, signature = sha1.getSHA1(self.token, sTimeStamp, sNonce, encrypt)
        if ret  != 0:
            return ret, None
        # if not signature == sMsgSignature:
        #     return ierror.WXBizMsgCrypt_ValidateSignature_Error, None
        pc = Prpcrypt(self.key)
        ret, xml_content = pc.decrypt(encrypt,self.appid)
        ret, content = xmlParse.extract_node(xml_content, out_node)
        return ret, content


def get_component_access_token(ticket):
    key = 'get_component_access_token'
    component_access_token = cache.get(key)

    if component_access_token:
        return component_access_token

    raw_data = '{"component_appid": "%s", "component_appsecret": "%s", "component_verify_ticket": "%s"}' % (WeChat_Open_AppId, WeChat_Open_AppSecret, ticket)
    r = requests.post('https://api.weixin.qq.com/cgi-bin/component/api_component_token',
                      data=raw_data)
    if r.status_code == requests.codes.ok:
        data = r.json()
        component_access_token = data.get('component_access_token', '')
        expires_in = int(data.get('expires_in', '7200'))
        if component_access_token:
            cache.set(key, component_access_token, expires_in)   # expires_in 7200
            return component_access_token
    return None


def get_pre_auth_code(component_access_token):
    key = 'get_pre_auth_code'
    pre_auth_code = cache.get(key)

    if pre_auth_code:
        return pre_auth_code

    raw_data = '{"component_appid": "%s"}' % WeChat_Open_AppId
    r = requests.post('https://api.weixin.qq.com/cgi-bin/component/api_create_preauthcode?component_access_token=%s' % component_access_token,
                      data=raw_data)
    if r.status_code == requests.codes.ok:
        data = r.json()
        pre_auth_code = data.get('pre_auth_code', '')
        expires_in = int(data.get('expires_in', '600'))
        if pre_auth_code:
            cache.set(key, pre_auth_code, expires_in)   # expires_in 600
            return pre_auth_code
    return None


def get_auth_info(auth_code, component_access_token, authorizer_appid):
    key1 = 'authorizer_access_token_for_authorizer_appid_%s' % authorizer_appid
    key2 = 'authorizer_refresh_token_for_authorizer_appid_%s' % authorizer_appid
    authorizer_access_token = cache.get(key1)
    authorizer_refresh_token = cache.get(key2)

    if authorizer_access_token and authorizer_refresh_token:
        return authorizer_access_token, authorizer_refresh_token

    raw_data = '''
        {
            "component_appid":"%s" ,
            "authorization_code": "%s"
        }
    ''' % (WeChat_Open_AppId, auth_code)

    r = requests.post('https://api.weixin.qq.com/cgi-bin/component/api_query_auth?component_access_token=%s' % component_access_token,data=raw_data)

    if r.status_code == requests.codes.ok:
        data = r.json()
        auth_info = data.get('authorization_info', '')
        authorizer_access_token = auth_info.get('authorizer_access_token', '')
        authorizer_refresh_token = auth_info.get('authorizer_refresh_token', '')
        expires_in = int(auth_info.get('expires_in', '7200'))
        cache.set(key1, authorizer_access_token, expires_in)
        cache.set(key2, authorizer_refresh_token, expires_in)
        return authorizer_access_token, authorizer_refresh_token
    return None, None


def refresh_token(component_access_token, authorizer_appid):
    key1 = 'authorizer_access_token_for_authorizer_appid_%s' % authorizer_appid
    key2 = 'authorizer_refresh_token_for_authorizer_appid_%s' % authorizer_appid
    authorizer_access_token = cache.get(key1)
    authorizer_refresh_token = cache.get(key2)

    if authorizer_access_token and authorizer_refresh_token:
        return authorizer_access_token, authorizer_refresh_token

    raw_data = '''
        {
            "component_appid":"%s",
            "authorizer_appid":"%s",
            "authorizer_refresh_token":"%s",
        }
    ''' % (WeChat_Open_AppId, authorizer_appid, authorizer_refresh_token)
    r = requests.post('https:// api.weixin.qq.com /cgi-bin/component/api_authorizer_token?component_access_token=%s' % component_access_token,data=raw_data)

    if r.status_code == requests.codes.ok:
        data = r.json()
        authorizer_access_token = data.get('authorizer_access_token', '')
        expires_in = int(data.get('expires_in', '7200'))
        authorizer_refresh_token = data.get('authorizer_refresh_token', '')
        cache.set(key1, authorizer_access_token, expires_in)
        cache.set(key2, authorizer_refresh_token, expires_in)
        return authorizer_access_token, authorizer_refresh_token
    return None, None


def add_material(access_token, media_url, media_type = 'thumb'):
    files = get_files(media_url)
    if files:
        r = requests.post('https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s' % (access_token, media_type), files=files)
        if r.status_code == requests.codes.ok:
            data = r.json()
            logger.info('data=%s' % data)
            media_id = data.get('media_id', '')
            return media_id
    return None


def convert_media_url(access_token, media_url):
    files = get_files(media_url)
    if files:
        r = requests.post('https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=%s' % access_token, files=files)
        if r.status_code == requests.codes.ok:
            data = r.json()
            logger.info('data=%s' % data)
            url = data.get('url', '')
            return url
    return None


def get_files(media_url):
    r = requests.get(media_url, stream=True)
    if r.status_code == requests.codes.ok:
        d = r.headers['content-disposition']
        fname = re.findall("filename=(.+)", d)
        fname = fname[0].split('"')
        if len(fname) > 1:
            fname = fname[1]
            files = {'media': (fname, r.content)}
            return files
    return None


def upload_news(access_token, data):
    r = requests.post('https://api.weixin.qq.com/cgi-bin/material/add_news?access_token=%s' % access_token, data=data)
    if r.status_code == requests.codes.ok:
        return r.json()
    return None


def find_img_url_list(html):
    replace_pattern = r'<[img|IMG].*?/>'  # img标签的正则式
    img_url_pattern = r'.+?src="(\S+)"'  # img_url的正则式
    replaced_img_url_list = []
    img_url_list = []
    need_replace_list = re.findall(replace_pattern, html)  # 找到所有的img标签
    for tag in need_replace_list:
        img_url = re.findall(img_url_pattern, tag)[0]
        if img_url.startswith('//'):      # maybe no schema,  <img src="//a.b.com/1.jpg">
            img_url += 'https:'
        img_url_list.append(img_url)  # 找到所有的img_url
    return img_url_list


def get_first_img_url(body):
    img_list = find_img_url_list(body)
    if img_list and len(img_list) > 0:
        return img_list[0]
    return ''


def convert_news_body(authorizer_access_token, body):
    replace_pattern = r'<[img|IMG].*?/>'  # img标签的正则式
    img_url_pattern = r'.+?P<url>src="(\S+)"'  # img_url的正则式
    need_replace_list = re.findall(replace_pattern, body)  # 找到所有的img标签
    for tag in need_replace_list:
        logger.info('tag=%s' % tag)
        media_url = re.findall(img_url_pattern, tag)[0]
        logger.info('media_url=%s' % media_url)
        media_url = convert_media_url(authorizer_access_token, media_url)
        logger.info('media_url=%s' % media_url)
        re.sub(img_url_pattern, media_url, tag)
        logger.info('tag=%s' % tag)
    return body


WeChat_Open_AppId = "wx75db18c650ebe235"
WeChat_Open_AppSecret = "4b9faf8bd863acbb99e5a9faed113f9b"
WeChat_Open_EncodingAESKey = "f0fba8d4165ecf6241f61e52381ec7c2Ylzjfww8989"