from django.db import models
from django.contrib.auth.models import User


class DictItemModel(models.Model):
    dictid = models.CharField(max_length=50, verbose_name='字典编码')
    dictname = models.CharField(max_length=100, verbose_name='字典名称')
    groupid = models.CharField(max_length=50, verbose_name='字典组编码')
    groupname = models.CharField(max_length=100, verbose_name='字典组名称')
    createdate = models.DateField(auto_now=True, verbose_name='创建日期')

    class Meta:
        verbose_name = '字典管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.dictname


class CollectModel(models.Model):
    linkname = models.CharField(max_length=200, verbose_name='链接名称')
    linkaddr = models.CharField(max_length=500, verbose_name='链接地址')
    status = models.ForeignKey(DictItemModel, verbose_name='状态', on_delete=models.CASCADE)
    remark = models.CharField(max_length=50, verbose_name='说明')
    owner = models.ForeignKey(User, verbose_name='创建人', on_delete=models.CASCADE)
    createdate = models.DateField(auto_now=True, verbose_name='创建日期')

    class Meta:
        verbose_name = '收藏管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.linkname


class MyCollectModel(models.Model):
    owner = models.ForeignKey(User, verbose_name='收藏者', on_delete=models.CASCADE)
    link = models.ForeignKey(CollectModel, verbose_name='链接名称', on_delete=models.CASCADE)  # 与CollectModel表的id关联，可确保唯一性
    collectdate = models.DateField(auto_now=True, verbose_name='收藏日期')

    class Meta:
        verbose_name = '我的收藏'
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.link


class StaticModel(models.Model):
    linkname = models.ForeignKey(CollectModel, verbose_name='链接名称', on_delete=models.CASCADE)
    clickcount = models.BigIntegerField(verbose_name='点击次数')
    collectcount = models.BigIntegerField(verbose_name='收藏次数')
    agreecount = models.BigIntegerField(verbose_name='点赞次数')

    class Meta:
        verbose_name = '统计管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.clickcount)

