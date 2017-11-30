import json

from flask import Flask, request
from flask_cors import CORS

from src.Database import DataBase
from src.Preformatter import Preformatter
from src.natural_to_sql import convert_natural_to_sql

APP = Flask(__name__)
CORS = CORS(APP)
APP.config['CORS_HEADERS'] = 'Content-Type'

db = DataBase()


@APP.route("/natural", methods=['POST'])
def natural():
    natural_request = request.form['natural_request']

    preformatter = Preformatter()
    preformatted_request = preformatter.preformat(natural_request)
    sql = convert_natural_to_sql(preformatted_request)
    return sql


@APP.route("/sql", methods=['POST'])
def sql():
    sql_request = request.form['sql_request']
    rows = list(db.execute(sql_request))
    return json.dumps(rows)


if __name__ == '__main__':
    APP.run()
