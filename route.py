from flask import Flask
from flask_restful import Resource, Api, reqparse

import pymysql
import json
import MySQLdb

from user import Login, UserAdd, User
from task import AddTask, GetTask, UpdateTask, DeleTask


db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
cursor =db. cursor()
#data = cursor.fetchone()

app = Flask(__name__)
api = Api(app)

class YearSort(Resource):
    def __init__(self):
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("year",  type=int)
        self.args = self.get_args.parse_args()

    def get(self):
        year = self.args["year"]
        obj = Init()
        res = obj.get(year)
        return res["data"]

class Year(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor =self.db. cursor()

    def get(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor = self.db.cursor()
        sql = '''select years from xyear'''
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        ll = []
        for one in res:
            ll.append(one[0])
        return ll


class Update(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor = self.db.cursor()
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("year",  type=int)
        self.get_args.add_argument("page",  type=int, default=1)
        self.get_args.add_argument("pageSize", type=int, default=10)
        self.get_args.add_argument("data",  type=str)
        self.args = self.get_args.parse_args()

    def charge_update(self, id):
        sql = '''select update_number from project where id = %d''' %id
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        return res

    def get(self):
        sdata = json.loads(self.args["data"])
        year = self.args["year"]

        charge_update= self.charge_update(sdata["id"])
        if charge_update[0] >= 3:
            return {"data": False, "message": "修改失败,最多修改三次"}

        update_number = charge_update[0] + 1

        obj = Init()
        data  = obj.get(year)
        if not sdata:
            return {"data": data["data"], "message": "您还没有输入数据"}
    
        sql = '''update project set project_time="%s" , project_number="%s" , area="%s" , billing_information="%s" , contact="%s" , tele="%s" , project_sort="%s" , order_content="%s" , norm="%s" , supplier="%s" , purchase_number=%d , original_price=%d , discount="%s" , sell_number=%d , sell_price=%d , tax="%s" , other_price=%d , profit="%s" , billing="%s" , back_money="%s" , billing_money="%s" , task_man="%s" , exe_man="%s" , common="%s" , year=%d, update_number=%d where id="%d" ''' % (sdata["project_time"], sdata["project_number"], sdata["area"], sdata["billing_information"], sdata["contact"], sdata["tele"],sdata["project_sort"], sdata['order_content'], sdata["norm"], sdata["supplier"], int(sdata["purchase_number"]), int(sdata["original_price"]), int(sdata["discount"][: -1]), int(sdata["sell_number"]), int(sdata["sell_price"]), int(sdata["tax"][: -1]), int(sdata["other_price"]), sdata["profit"], sdata["billing"], sdata["back_money"], sdata["billing_money"], sdata["task_man"], sdata["exe_man"], sdata["common"], year, update_number, int(sdata["id"]))
        self.cursor.execute(sql)
        self.db.commit()
        return {"data": data["data"], "message": "保存成功"}


class Add(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor =self.db. cursor()
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("data",  type=str)
        self.get_args.add_argument("year",  type=int)
        self.args = self.get_args.parse_args()

    def get(self):
        sdata = json.loads(self.args["data"])
        year = self.args["year"]

        obj = Init()
        data  = obj.get(year)
        if not sdata:
            return {"data": data["data"], "message": "您还没有输入数据"}

        for one in sdata:
            sql = '''insert into project (project_time, project_number, area, billing_information, contact, tele, project_sort, order_content, norm, supplier, purchase_number, original_price, discount, sell_number, sell_price,  tax, other_price, profit, billing, back_money, billing_money, task_man, exe_man, common, year, update_number) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %f,%f, '%s', %f, %f, '%s', %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, %d )''' % (one["project_time"], one["project_number"], one["area"], one["billing_information"], one["contact"], one["tele"], one["project_sort"], one['order_content'], one["norm"], one["supplier"], float(one["purchase_number"]), float(one["original_price"]), one["discount"], float(one["sell_number"]), float(one["sell_price"]), one["tax"], float(one["other_price"]), one["profit"], one["billing"], one["back_money"], one["billing_money"] if one ["billing_money"] else "1", one["task_man"], one["exe_man"], one["common"], year, 0)
            self.cursor.execute(sql)
            self.db.commit()
            return {"data": data["data"], "message": "保存成功"}
            #except:
            #    return {"data": data["data"], "message": "保存失败"}


class Init(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor = self.db.cursor()
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("year",  type=int)
        self.get_args.add_argument("page",  type=int, default=1)
        self.get_args.add_argument("pageSize",  type=int, default=10)
        self.args = self.get_args.parse_args()

    def total_page(self, offset):
        sql = '''select count(id) from project'''
        self.cursor.execute(sql)
        number = self.cursor.fetchone()
        return number[0]

    def get(self, year=2019):
        year = self.args["year"]
        page = self.args["page"]
        pagesize = self.args["pageSize"]
        total_page = self.total_page(pagesize)

        start_page = (page-1) * pagesize
        sql = '''select * from project where year=%d order by project_number desc limit %d, %d''' % (year, start_page, pagesize)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        ll = []
        for one in res:
            dd = {}
            dd["id"] = one[0]
            dd["project_time"] = one[1]
            dd["project_number"] = one[2]
            dd["area"] = one[3]
            dd["billing_information"] = one[4]
            dd["contact"] = one[5]
            dd["tele"] = one[6]
            dd["project_sort"] = one[7]
            dd["order_content"] = one[8]
            dd["norm"] = one[9]
            dd["supplier"] = one[10]
            dd["purchase_number"] = one[11]
            dd["original_price"] = one[12]
            dd["discount"] = one[13] + "%"
            dd["total_price"] = round(one[11] * abs(one[12]) * float(one[13]) / 100, 2)

            dd["sell_number"] = one[14]
            dd["sell_price"] = one[15]
            dd["sell_total_price"] = round(one[14] * one[15], 2)

            dd["tax"] = one[16] + "%"
            dd["other_price"] = one[18]
            dd["price_after_tax"] = round(dd["sell_total_price"]  * int(one[16]) / 100, 2)

            dd["profit"] =  round(dd["price_after_tax"] - one[18] - dd["total_price"], 2)
            dd["billing"] = one[20]
            dd["back_money"] = one[21]
            dd["billing_money"] = one[22]
            dd["task_man"] = one[23]
            dd["exe_man"] = one[24]
            dd["common"] = one[25]
            dd["create_time"] = str(one[27])
            dd["update_number"] = one[28]
            ll.append(dd)
        res = {}
        res["data"] = ll
        res["total_page"] = total_page
        return res


api.add_resource(Init, '/init')
api.add_resource(Add, '/init/add')
api.add_resource(Update, '/init/update')
api.add_resource(Year, '/init/year')
api.add_resource(Login, '/init/login')
api.add_resource(YearSort, '/init/yearsort')
api.add_resource(UserAdd, '/init/useradd')
api.add_resource(User, '/init/getuser')
api.add_resource(AddTask, '/init/addtask')
api.add_resource(GetTask, '/init/gettask')
api.add_resource(UpdateTask, '/init/updatetask')
api.add_resource(DeleTask, '/init/deletetask')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
