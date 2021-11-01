import pymysql
from flask import Flask

con = pymysql.connect(host='localhost', user='root', passwd='Aco556787879', db='sql_intro')
cursor = con.cursor()

server = Flask(__name__, static_url_path='', static_folder='dist')
port_number = 3002