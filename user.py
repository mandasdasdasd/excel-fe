from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse

import pymysql
import json

import MySQLdb

db = pymysql.connect("159.226.193.219","mysql","mysql","ysman" )
cursor =db. cursor()

class User(Resource):

    def __init__(self):
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("user",  type=str)
        self.get_args.add_argument("pwd",  type=str)
        self.args = self.get_args.parse_args() 

    def get(self):
        user = self.args["user"]
        pwd = self.args["pwd"]

        sql = '''select * from user where user ="%s" and pwd="%s" and status=1 ''' % (user, pwd)
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            resp=Response("1")
            resp.set_cookie("role", str(res[0][5]))
            resp.set_cookie("name", str(res[0][1]))
            return resp
        else:
            return 0
