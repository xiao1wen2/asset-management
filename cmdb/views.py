# -*- coding: utf-8 -*-
import json
import os
import xlrd
from django.db.models import Q
from django.views.generic import View, TemplateView
from django.http import JsonResponse, HttpResponse, QueryDict
from utils.baseviews import BaseAPIView, BaseListView
from .models import Idc, Rack, Server
from django.shortcuts import render
# Create your views here.


class IdcView(BaseListView):
    """机房的列表页/详情页, 增删改查"""
    model = Idc
    template_name = 'cmdb/idcs.html'
    template_detail = 'cmdb/idc_detail.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__contains=search) | Q(address__contains=search))
        qs = [i.to_dict for i in queryset]
        return qs


class APIIdcView(BaseAPIView):
    """"机房的API: 查询"""
    model = Idc


class RackView(BaseListView):
    """机柜的列表页/详情页, 增删改查"""
    model = Rack
    template_name = 'cmdb/racks.html'
    template_detail = 'cmdb/rack_detail.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        idc_id = self.request.GET.get('idc_id')
        if idc_id:
            queryset = queryset.filter(idc_id=idc_id)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__contains=search) | Q(number__contains=search) | Q(size__contains=search))
        qs = [i.to_dict for i in queryset]
        return qs


class APIRackView(BaseAPIView):
    """"机柜的API: 查询"""
    model = Rack


class ServerView(BaseListView):
    """服务器的列表页/详情页, 增删改查"""
    model = Server
    template_name = 'cmdb/servers.html'
    template_detail = 'cmdb/server_detail.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        rack_id = self.request.GET.get('rack_id')
        if rack_id:
            queryset = queryset.filter(rack_id=rack_id)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__contains=search) | Q(ip__contains=search))
        qs = [i.to_dict for i in queryset]
        return qs


class APIServerView(BaseAPIView):
    """"机柜的API: 查询, 自动采集的信息录入"""
    model = Server

    def post(self, request, *args, **kwargs):
        data = QueryDict(request.body).dict()
        name = data.get('hostname')
        uuid = data.get('uuid')
        server_type = data.get('server_type')
        cpu = data.get('server_cpu')
        memory = data.get('server_mem')
        disk = data.get('server_disk')
        daq = json.dumps(data)
        server_data = {
            'name': name,
            'cpu': cpu,
            'memory': memory,
            'disk': disk,
            'uuid': uuid,
            'server_type': server_type,
            'daq': daq
        }
        qs_instance = self.model.objects.filter(uuid=uuid, server_type=server_type)
        if qs_instance:
            qs_instance.update(**server_data)
            qs_instance.first().save()
        else:
            self.model.objects.create(**server_data)
        return JsonResponse({})


class DashBoardView(TemplateView):
    """"DashBoard页面"""
    template_name = 'dashboard.html'


class APIDashBoardView(View):
    """DashBoard页面需要的数据"""
    def get(self, request, *args, **kwargs):
        data = {}
        data_idc_servers = []
        data_site = []
        idc_list = Idc.objects.all()
        for idc in idc_list:
            servers = 0
            site_idc = {}
            racks = idc.rack_set.all()
            total_site = racks.count()*10
            for rack in racks:
                servers += rack.to_dict.get('servers').get('count')
            data_idc_servers.append(
                [idc.name, servers]
            )
            if total_site > 0:
                site_idc['name'] = idc.name
                site_idc['total_site'] = total_site
                site_idc['site'] = servers
                data_site.append(site_idc)
        data['data_idc_servers'] = data_idc_servers
        data['data_site'] = data_site
        data['count'] = {
            'idcs': idc_list.count(),
            'racks': Rack.objects.count(),
            'servers': Server.objects.count()
        }
        return JsonResponse({'data': data})


class Insert_from_excel(View):
    # def upload(self, request):
    #     # 上传文件
    #     if request.method == "POST":
    #         print(request, '------------------------')
    #         # user = request.POST.get('user')
    #         # fafafa = request.POST.get('fafafa')
    #         # file = request.POST.get('servers')
    #
    #         file = request.FILES.get('servers')
    #         # print(obj.name,obj.size) #读取文件名称和大小，返回后台
    #         # print(user,fafafa)
    #         file_path = os.path.join('static', 'upload', file.name)
    #
    #         f = open(file_path, 'wb')
    #         for chunk in file.chunks():
    #             f.write(chunk)
    #         f.close()
    #         models.Img.objects.create(path=file_path)
    #
    #         ret = {'status': True, 'path': file_path}
    def post(self, request, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_dir = os.path.join(base_dir, 'static/services/')
        # file = request.FILES.get('servers')
        # file.save(file_dir + file)
        File = request.FILES.get("servers", None)
        if File is None:
            return HttpResponse("没有需要上传的文件")
        else:
            # 打开特定的文件进行二进制的写操作
            # print(os.path.exists('/temp_file/'))
            with open(file_dir + "{}".format(File.name), 'wb+') as f:
                # 分块写入文件
                for chunk in File.chunks():
                    f.write(chunk)
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        excelpath = os.path.join(base, 'static/services/serverexample.xlsx')
        book = xlrd.open_workbook(excelpath)
        sheet = book.sheet_by_index(0)
        row = sheet.nrows
        col = sheet.ncols
        field = ['name', 'remark', 'asset_number', 'uuid', 'under_name', 'cpu', 'memory', 'disk', 'ip', 'business', 'status', 'rack_id']
        for i in range(1, row):
            vaule = []
            for j in range(0, col):
                vaule.append(sheet.cell(i, j).value)
            data = {}
            leng = len(vaule)
            for s in range(0, leng):
                if s == 5:
                    data[field[s]] = str(int(vaule[s]))
                if s == 10:
                    data[field[s]] = int(vaule[s])
                elif s == 11:
                    data[field[s]] = int(vaule[s])
                else:
                    data[field[s]] = vaule[s]

            Server.objects.create(**data)

        return render(request, 'cmdb/servers.html')

