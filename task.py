from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import pymysql
import json
import MySQLdb

from user import Login, UserAdd, User


app = Flask(__name__)
api = Api(app)


class UpdateTask(Resource):
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

        obj = GetTask()
        data  = obj.get(year)

        sql = '''update task set task='%s', user='%s', status='%s' where id =%d ''' % (sdata["task"], sdata["user"], int(sdata["status"]), int(sdata["id"]))
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        return {"data": data, "message": "成功"}


class AddTask(Resource):
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
        userid = request.cookies.get('userid')

        obj = GetTask()
        data  = obj.get(year)
        if not sdata:
            return {"data": data["data"], "message": "您还没有输入数据"}

        for one in sdata:
            sql = '''insert into task (task, user, status, year, userid) values ('%s', '%s', %d, %d, %d)''' % (one["task"], one["user"] if one["user"] else "其他", int(one["status"]), year, int(userid))
            print(sql)
            self.cursor.execute(sql)
            self.db.commit()
        return {"data": data, "message": "成功"}


class GetTask(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor = self.db.cursor()
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("page",  type=int, default=1)
        self.get_args.add_argument("pageSize",  type=int, default=10)
        self.get_args.add_argument("year",  type=int)
        self.args = self.get_args.parse_args()

    def total_page(self, offset, userid, year):
        sql = '''select count(id) from task where userid = %d and year= %d''' % (int(userid), year)
        self.cursor.execute(sql)
        number = self.cursor.fetchone()
        return number[0]

    def get(self, year=2019):
        userid = request.cookies.get('userid')
        year = self.args["year"]
        page = self.args["page"]
        pagesize = self.args["pageSize"]
        total_page = self.total_page(pagesize, userid, year)

        start_page = (page-1) * pagesize
        sql = '''select * from task where year = %d and userid = %d order by create_time desc limit %d, %d''' % (year, int(userid), start_page, pagesize)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        ll = []
        for one in res:
            u = one[2]
            if not one[2] or one[2] == "None":
                u = "其他"
            dd = {}
            dd["id"] = one[0]
            dd["task"] = one[1]
            dd["user"] = u
            dd["create_time"] = str(one[3])
            dd["status"] = str(one[4])
            ll.append(dd)
        res = {}
        res["data"] = ll
        res["total_page"] = total_page
        return res
