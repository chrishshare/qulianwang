from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from qlwang.models import DictItemModel, CollectModel, MyCollectModel, StaticModel, WXUser
import json
from django.core.serializers.json import DjangoJSONEncoder

from qlwang.utils import get_user_info, result_dict, user_to_payload, payload_to_user
from qlwang.wxcrypt import WXBizDataCrypt
from qlwang.django_jwt_session_auth import jwt_login


@csrf_exempt
def login(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        info = get_user_info(code)
        crypt = WXBizDataCrypt(appid='wxb152587abf2c44f0', session_key=info.get('session_key'))
        user_info = crypt.decrypt(encrypted_data=request.POST.get('encryptedData'), iv=request.POST.get('iv'))
        db_user = WXUser.objects.filter(openid=user_info.get('openId'))
        if not db_user.exists():
            wx = WXUser.objects.create(openid=user_info.get('openId'), nickname=user_info.get('nickName'),
                                  gender=user_info.get('gender'), language=user_info.get('language'),
                                  city=user_info.get('city'), province=user_info.get('province'),
                                  country=user_info.get('country'), avatarUrl=user_info.get('avatarUrl'))
            wx.save()
        result = [{'retcode': 0, 'retmsg': '成功', 'userinfo': user_info}]
        return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder, ensure_ascii=False))

    else:
        return HttpResponse(-1, '不支持该方法')


def qry_collect(request):
    if request.method == 'GET':
        print(request.GET)
        openid = request.GET.get('openid')
        cotype = request.GET.get('cotype')
        if 'my' == cotype:
            queryset = CollectModel.objects.filter(owner=WXUser.objects.get(openid=openid)).values('linkaddr', 'linkname', 'remark', 'createdate', 'status')
            print(queryset)
            result = result_dict(0, '查询成功', queryset)
            return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder, ensure_ascii=False))
        else:
            queryset = CollectModel.objects.filter(status='公开').values('linkaddr', 'linkname', 'remark', 'createdate', 'status')
            print(queryset)
            result = result_dict(0, '查询成功', queryset)
            return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder, ensure_ascii=False))

    else:
        pass


@csrf_exempt
def add_url(request):
    print(request.GET)
    if request.method == 'GET':
        openid = request.GET.get('openid')
        linkname = request.GET.get('linkname')
        linkaddr = request.GET.get('linkaddr')
        remark = request.GET.get('remark')
        status = request.GET.get('status')
        db_status = ''
        if status == 'true':
            db_status = '公开'
        else:
            db_status = '私有'
        db_user = WXUser.objects.filter(openid=openid)
        if not db_user.exists():
            result = result_dict(-1, '用户不存在')
            return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder, ensure_ascii=False))
        else:
            col = CollectModel.objects.create(linkname=linkname, linkaddr=linkaddr, status=db_status, remark=remark, owner=WXUser.objects.get(openid=openid))
            col.save()
            result = result_dict(0, '创建成功')
            return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder, ensure_ascii=False))

    else:
        print(request)
        pass
