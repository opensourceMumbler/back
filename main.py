from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.schema import HumanMessage
from flask import Flask, request
import datetime
import pymysql
import os

load_dotenv()
llm = OpenAI()

db_connection = pymysql.connect(
    user = 'admin',
    passwd=os.environ['db_pw'],
    host=os.environ['db_url'],
    db='mumbler',
    charset='utf8'
)


@app.route('/search')
def main_get():
    db = db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    user = request.args.get("user")
    now = request.args.get("now")
    now_start = datetime.datetime.striptime(now, '%Y-%m-%d %H:%M:%S')
    now_start.replace(hour=0, minute=0, second=0)

    query = 'SELECT * FROM mumbles where user = {user} and timestamp > {now_start} and timestamp < {now}'
    cursor.excute(query)
    result = cursor.fetchall()

    context = "라는 일기에 대해 감정분석을 해줘"
    report = llm.invoke(result+context)
    
    return report


@app.rout('/insert', methods=['POST', 'GET'])
def insert():
    db = db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        form = request.form

    query = 'INSERT INTO mumbles (mumble, user, timestamp) VALUES ({form.mumbles}, {form.user}, {now})'
    cursor.excute(query)
    db.commit()
    db.close()
    
