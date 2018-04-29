from django.contrib import admin
from qlwang.models import CollectModel, MyCollectModel, DictItemModel, StaticModel, WXUser


admin.site.register(DictItemModel)
admin.site.register(CollectModel)
admin.site.register(MyCollectModel)
admin.site.register(StaticModel)
admin.site.register(WXUser)
