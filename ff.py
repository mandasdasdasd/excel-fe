from flask import Flask
from flask_restful import Resource, Api, reqparse

import pymysql
import json
 
db = pymysql.connect("159.226.193.219","mysql","mysql","ysman" )
cursor = db.cursor()
#cursor.execute("SELECT VERSION()")
#data = cursor.fetchone()


app = Flask(__name__)
api = Api(app)

class Save(Resource):
    def __init__(self):
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("data",  type=str)
        self.args = self.get_args.parse_args()

    def get(self):
        data = self.args["data"]
        for one in json.loads(data):
            print(one["sex"])
            #sql = '''insert into table_name (sex, name, age) values (%d, %d, %d)''' % ()

class HelloWorld(Resource):
    def get(self):
        return [
                {'sex': 1, 'age': 2, 'name': 3},
                {'sex': 1, 'age': 2, 'name': 3},
                {'sex': 1, 'age': 2, 'name': 3},
                {'sex': 1, 'age': 2, 'name': 3},
                {'sex': 1, 'age': 2, 'name': 3},
                {'sex': 1, 'age': 2, 'name': 3},
                ]


api.add_resource(HelloWorld, '/init')
api.add_resource(Save, '/init/add')

if __name__ == '__main__':
    app.run(debug=True)
