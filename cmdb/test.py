import os
import xlrd
from django.views import View
import pymysql





# class ins(View):
#     def post(self):
#         # base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         # excelpath = os.path.join(base, 'static/services/serverexample.xlsx')
#         # book = xlrd.open_workbook(excelpath)
#         # sheet = book.sheet_by_index(0)
#         # row = sheet.nrows
#         # col = sheet.ncols
#         # field = ['name', 'remark', 'asset_number', 'uuid', 'under_name', 'cpu', 'memory', 'disk', 'ip', 'business', 'status','rack_id']
#         # number = 0
#         # for i in range(1, row):
#         #     vaule = []
#         #     for j in range(0, col):
#         #         vaule.append(sheet.cell(i, j).value)
#         #     # data = {}
#         #     # for s in field:
#         #     #     if number == 12:
#         #     #         number = 0
#         #     #     data[s] = vaule[number]
#         #     #     number += 1
#         # print(vaule)
#         #     # Server.objects.create(**data)
#         # con = pymysql.connect('127.0.0.1', 'root', '123.com', 'ops', 3306)
#         # cousor = con.cursor()
#         # sql = 'replace into cmdb_server(name, remark, asset_number, uuid, under_name, cpu, memory, disk, ip, business, status, rack_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#         # leng = len(vaule)
#         # param = []
#         # for i in range(0, leng):
#         #     if i == 10:
#         #         param.append(int(vaule[i]))
#         #     elif i == 11:
#         #         param.append(int(vaule[i]))
#         #     else:
#         #         param.append(str(vaule[i]))
#         # print(param)
#         # cousor.execute(sql, param)
#         # con.commit()
#         # cousor.close()
#         # con.close()
#         base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#         excelpath = os.path.join(base, 'static/services/serverexample.xlsx')
#         book = xlrd.open_workbook(excelpath)
#         sheet = book.sheet_by_index(0)
#         row = sheet.nrows
#         col = sheet.ncols
#         field = ['name', 'remark', 'asset_number', 'uuid', 'under_name', 'cpu', 'memory', 'disk', 'ip', 'business', 'status', 'rack_id']
#         for i in range(1, row):
#             vaule = []
#             for j in range(0, col):
#                 vaule.append(sheet.cell(i, j).value)
#             data = {}
#
#             leng = len(vaule)
#             for s in range(0, leng):
#                 if s == 10:
#                     data[field[s]] = int(vaule[s])
#                 elif s == 11:
#                     data[field[s]] = int(vaule[s])
#                 else:
#                     data[field[s]] = vaule[s]
#
#             print(data)
#
#
# if __name__ == '__main__':
#     po = ins()
#     po.post()
#     # a = {'name': '2.2.2.15', 'remark': 1.0, 'asset_number': 'Y20200531', 'uuid': 1.0, 'under_name': '宋江', 'cpu': 1.0, 'memory': '12G', 'disk': '11t', 'ip': '2.2.2.15', 'business': 1.0, 'status': '2.2.2.15', 'rack_id': 1.0}
#     # print(**a)
#

a = {"data": [{"id": 1, "name": "bj-rack1", "create_time": "2020-05-21T12:38:16.417", "update_time": "2020-05-21T12:38:16.417", "remark": 1, "idc_id": 1, "number": "1", "size": "10"}], "count": 1}
print(a['data'])