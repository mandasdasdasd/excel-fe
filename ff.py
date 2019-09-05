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
        return res

class Year(Resource):
    def get(self):
        db = pymysql.connect("159.226.193.219","mysql","mysql","ysman" )
        acursor = db.cursor()
        sql = '''select years from xyear'''
        acursor.execute(sql)
        res = acursor.fetchall()
        ll = []
        for one in res:
            ll.append(one[0])
        return ll

class Add(Resource):
    def __init__(self):
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("data",  type=str)
        self.get_args.add_argument("year",  type=int)
        self.args = self.get_args.parse_args()

    def get(self):
        cursor = db.cursor()
        sdata = json.loads(self.args["data"])
        year = self.args["year"]

        obj = Init()
        data  = obj.get(year)
        if not sdata:
            return {"data": data, "message": "您还没有输入数据"}

        try:
            for one in sdata:
                sql = '''insert into hh (year, name, input, output, discount, number, status, people) values (%d, '%s', %d, %d, %f, %d,  '%s', '%s')''' % (int(one["year"]), one["vname"], int(one["input"]), int(one["output"]), float(one["discount"]), int(one["number"]), one["status"], one['people'])
                cursor.execute(sql)
                db.commit()
                return {"data": data, "message": "保存成功"}
        except:
            return {"data": data, "message": "保存失败"}

class Init(Resource):
    def __init__(self):
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("year",  type=int)
        self.args = self.get_args.parse_args()

    def get(self, year=2019):
        year = self.args["year"]

        sql = '''select * from hh where year=%d''' % year
        cursor.execute(sql)
        res = cursor.fetchall()
        ll = []
        for one in res:
            dd = {}
            dd["id"] = one[0]
            dd["vname"] = one[1]
            dd["input"] = one[2]
            dd["output"] = one[3]
            dd["discount"] = one[4]
            dd["profit"] = (one[3] - one[2]*one[4]) * one[5]
            dd["number"] = one[5]
            dd["status"] = one[6] if one[6] !="None" else "无标记"
            dd["year"] = one[7]
            dd["people"] = one[8]
            ll.append(dd)
        return ll


api.add_resource(Init, '/init')
api.add_resource(Add, '/init/add')
api.add_resource(Year, '/init/year')
api.add_resource(YearSort, '/init/yearsort')

if __name__ == '__main__':
    app.run(debug=True)
