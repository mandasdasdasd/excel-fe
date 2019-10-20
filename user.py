from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse

import pymysql
import json

import MySQLdb
from utils import Encryption


class Login(Resource):

    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor =self.db.cursor()

        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("user",  type=str)
        self.get_args.add_argument("pwd",  type=str)
        self.args = self.get_args.parse_args() 

    def get(self):
        user = self.args["user"]
        pwd = self.args["pwd"]

        encryption_obj = Encryption()
        encrptstr= encryption_obj.hmac_md5(pwd)

        sql = '''select * from user where user ="%s" and pwd="%s" and status=1''' % (user, encrptstr)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if res:
            resp=Response("1")
            name = res[0][2]
            privilege = res[0][2]
            resp.set_cookie("role", str(res[0][5]))
            resp.set_cookie("userid", str(res[0][0]))
            resp.set_cookie("user", name)
            resp.set_cookie("privilege", privilege)
            return resp
        else:
            return 0


class UserAdd(Resource):

    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor =self.db.cursor()

        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("data",  type=str)
        self.args = self.get_args.parse_args() 

    def get(self):
        privilege = request.cookies.get('privilege')
        if privilege != "admin":
            return {}

        data = json.loads(self.args["data"])
        for one in data:
            print(one)
            sql = '''insert into user (name, user, pwd, tele_number, role, sex, status) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")''' % (one["name"], one["user"], one["pwd"], one["tele"], one["role"], one["sex"], one["status"])
            self.cursor.execute(sql)
            self.db.commit()
            return {"data": True , "message": "保存成功"}



class User(Resource):

    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor =self.db.cursor()
        self.get_args = reqparse.RequestParser()
        self.args = self.get_args.parse_args() 

    def get(self):
        privilege = request.cookies.get('privilege')
        if privilege != "admin":
            return {}

        sql = '''select * from user'''
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        ulist = []
        for one in res:
            udict = {}
            udict["name"] = one[1]
            udict["user"] = one[2]
            udict["pwd"] = one[3]
            udict["tele"] = one[4]
            udict["role"] = one[5]
            udict["sex"] = one[6]
            udict["create_time"] = str(one[7])
            udict["status"] = one[8]
            ulist.append(udict)
        return ulist
