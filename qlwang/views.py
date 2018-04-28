from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from qlwang.models import DictItemModel, CollectModel, MyCollectModel, StaticModel
import json
from django.core.serializers.json import DjangoJSONEncoder


def result_dict(retcode, retmsg, dictdata=''):
    tmp = dict()
    tmp['retcode'] = retcode
    tmp['retmsg'] = retmsg
    tmp['list'] = list(dictdata)
    return tmp


def add_url(request):
    if request.method == 'GET':
        print(request.GET)
        # qryresult =
    else:
        pass


def qry_collect(request):
    if request.method == 'GET':
        try:
            qryresult = CollectModel.objects.all().values('linkname',
                                                             'linkaddr',
                                                             'remark',
                                                             'createdate',
                                                             'status__dictid',
                                                             'status__dictname')
            # aa = json.dumps(list(qryresult), cls=DjangoJSONEncoder, ensure_ascii=False)
            result = result_dict(0, '查询成功', qryresult)
            print(result)
            return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder, ensure_ascii=False))
        except Exception as e:
            result = result_dict(0, '查询结果异常')
            return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder, ensure_ascii=False))

    else:
        pass
