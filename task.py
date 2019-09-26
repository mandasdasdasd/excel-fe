from flask import Flask
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
        self.args = self.get_args.parse_args()

    def get(self):
        sdata = json.loads(self.args["data"])

        obj = GetTask()
        data  = obj.get()

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
        self.args = self.get_args.parse_args()

    def get(self):
        sdata = json.loads(self.args["data"])

        obj = GetTask()
        data  = obj.get()
        if not sdata:
            return {"data": data["data"], "message": "您还没有输入数据"}

        for one in sdata:
            sql = '''insert into task (task, user, status) values ('%s', '%s', %d)''' % (one["task"], one["user"], int(one["status"]))
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
        self.args = self.get_args.parse_args()

    def total_page(self, offset):
        sql = '''select count(id) from project'''
        self.cursor.execute(sql)
        number = self.cursor.fetchone()
        return number[0]

    def get(self, year=2019):
        page = self.args["page"]
        pagesize = self.args["pageSize"]
        total_page = self.total_page(pagesize)

        start_page = (page-1) * pagesize
        sql = '''select * from task order by create_time desc limit %d, %d''' % (start_page, pagesize)
        print(sql)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        ll = []
        for one in res:
            dd = {}
            dd["id"] = one[0]
            dd["task"] = one[1]
            dd["user"] = one[2]
            dd["create_time"] = str(one[3])
            dd["status"] = str(one[4])
            ll.append(dd)
        res = {}
        res["data"] = ll
        res["total_page"] = total_page
        return res
