from django.db import models
import json


class BaseModel(models.Model):
    '''
       基础表(抽象类)
    '''
    name = models.CharField(default='', null=True, blank=True, max_length=128, verbose_name='名字')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    remark = models.TextField(default='', null=True, blank=True, verbose_name='备注')

    @property
    def to_dict_base(self):
        ret = dict()
        for attr in [f.name for f in self._meta.fields]:
            value = getattr(self, attr)
            ret[attr] = value
        return ret

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['-id']


class Idc(BaseModel):
    address = models.CharField(max_length=256, verbose_name='地址')

    class Meta:
        ordering = ['-id']
        unique_together = ('name',)

    @property
    def to_dict(self):
        ret = self.to_dict_base
        objects = self.rack_set.all()
        ret['racks'] = {'data': [obj for obj in objects.values()], 'count': objects.count()}
        return ret


class Rack(BaseModel):
    idc = models.ForeignKey(Idc, default='', null=True, blank=True, on_delete=models.SET_DEFAULT, verbose_name='所属机房')
    number = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='编号')
    size = models.CharField(default='', max_length=8, null=True, blank=True, verbose_name='U型')

    class Meta:
        ordering = ['-id']
        unique_together = ('name', 'idc')

    @property
    def to_dict(self):
        ret = self.to_dict_base
        idc = getattr(self, 'idc')
        idc_data = idc.to_dict if idc else {}
        ret['idc'] = idc_data
        objects = self.server_set.all()
        ret['servers'] = {'data': [obj for obj in objects.values()], 'count': objects.count()}
        return ret


class Server(BaseModel):
    STATUS = (
        (0, u'下线'),
        (1, u'在线'),
    )
    rack = models.ForeignKey(Rack, default='', null=True, blank=True, on_delete=models.SET_DEFAULT, verbose_name='所属机柜')
    asset_number = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='资产编号')
    uuid = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='uuid')
    under_name = models.CharField(default='', max_length=32, null=True, blank=True, verbose_name='所属名下')
    cpu = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='CPU')
    memory = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='内存')
    disk = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='磁盘大小')
    ip = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='ip地址')
    business = models.CharField(default='', max_length=64, null=True, blank=True, verbose_name='业务线')
    server_type = models.CharField(default='', max_length=128, null=True, blank=True, verbose_name='服务器类型')
    daq = models.TextField(default='', null=True, blank=True, verbose_name='数据采集')
    status = models.IntegerField(default=1, choices=STATUS, verbose_name='运行状态')

    class Meta:
        ordering = ['-id']
        unique_together = ('uuid', 'server_type')

    @property
    def to_dict(self):
        ret = self.to_dict_base
        rack = getattr(self, 'rack')
        rack_data = rack.to_dict if rack else {}
        ret['rack'] = rack_data
        daq = eval(self.daq) if self.daq else ''
        ret['daq'] = daq
        ret['daq_json'] = json.dumps(daq)
        return ret
