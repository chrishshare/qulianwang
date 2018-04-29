from qlwang.models import WXUser
import json
from django.core.serializers.json import DjangoJSONEncoder
import requests
import datetime


def user_to_payload(user):
    exp = datetime.datetime.now() + datetime.timedelta(seconds=3600 * 7)
    return {
        'user_id': str(user),
        'exp': exp
    }


def payload_to_user(payload):
    if not payload:
        return None
    user_id = payload.get('user_id')
    user = WXUser.objects.get(openid=user_id)
    return user


def get_user_info(code):
    # appid=wxb152587abf2c44f0
    # secret = 1f71fac86d6240b4888fec9507b72394
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wxb152587abf2c44f0&secret=1f71fac86d6240b4888fec9507b72394&js_code=' + code +'&grant_type=authorization_code'
    resonse = requests.get(url=url)
    return resonse.json()


def result_dict(retcode, retmsg, dictdata=''):
    tmp = dict()
    tmp['retcode'] = retcode
    tmp['retmsg'] = retmsg
    if isinstance(dictdata, str):
        tmp['list'] = dictdata
    else:
        tmp['list'] = list(dictdata)
    return tmp

