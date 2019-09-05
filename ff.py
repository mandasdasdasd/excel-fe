from flask import Flask
from flask_restful import Resource, Api, reqparse

import pymysql
import json
 
db = pymysql.connect("159.226.193.219","mysql","mysql","ysman" )
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
        self.db = pymysql.connect("159.226.193.219","mysql","mysql","ysman" )
        self.cursor =self.db. cursor()

    def get(self):
        self.db = pymysql.connect("159.226.193.219","mysql","mysql","ysman" )
        self.cursor = self.db.cursor()
        sql = '''select years from xyear'''
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        ll = []
        for one in res:
            ll.append(one[0])
        return ll

class Add(Resource):
    def __init__(self):
        self.db = pymysql.connect("159.226.193.219","mysql","mysql","ysman" )
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

        try:
            for one in sdata:
                sql = '''insert into hh (year, name, input, output, discount, number, status, people) values (%d, '%s', %f, %f, %f, %d,  '%s', '%s')''' % (int(one["year"]), one["vname"], float(one["input"]), float(one["output"]), float(one["discount"]), int(one["number"]), one["status"], one['people'])
                self.cursor.execute(sql)
                self.db.commit()
                return {"data": data["data"], "message": "保存成功"}
        except:
            return {"data": data["data"], "message": "保存失败"}

class Init(Resource):
    def __init__(self):
        self.db = pymysql.connect("159.226.193.219","mysql","mysql","ysman" )
        self.cursor = self.db.cursor()
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("year",  type=int)
        self.get_args.add_argument("page",  type=int, default=1)
        self.get_args.add_argument("pageSize",  type=int, default=10)
        self.args = self.get_args.parse_args()

    def total_page(self, offset):
        sql = '''select count(id) from hh'''
        self.cursor.execute(sql)
        number = self.cursor.fetchone()
        return number[0]

    def get(self, year=2019):
        year = self.args["year"]
        page = self.args["page"]
        pagesize = self.args["pageSize"]
        print(pagesize) 
        total_page = self.total_page(pagesize)

        start_page = (page-1) * pagesize
        sql = '''select * from hh where year=%d order by create_time desc limit %d, %d''' % (year, start_page, pagesize)
        print(sql)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        ll = []
        for one in res:
            dd = {}
            dd["id"] = one[0]
            dd["vname"] = one[1]
            dd["input"] = one[2]
            dd["output"] = one[3]
            dd["discount"] = one[4]
            dd["profit"] = round((one[3] - one[2]*one[4]) * one[5], 2)
            dd["number"] = one[5]
            dd["status"] = one[6] if one[6] !="None" else "无标记"
            dd["year"] = one[7]
            dd["people"] = one[8]
            dd["createtime"] = str(one[9])
            ll.append(dd)
        res = {}
        res["data"] = ll
        res["total_page"] = total_page
        return res


api.add_resource(Init, '/init')
api.add_resource(Add, '/init/add')
api.add_resource(Year, '/init/year')
api.add_resource(YearSort, '/init/yearsort')

if __name__ == '__main__':
    app.run(debug=True)
