#coding:utf8
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask.ext.redis import FlaskRedis
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:5418854188@127.0.0.1:3306/movie?charset=utf8"
app.config["SQLACLHEMY_TRACK_MODIFICATIONS"] = True #追踪对象的修改
app.config["SECRET_KEY"] = 'd97073f46b214e9e9d890c41af49886e'
app.config["REDIS_URL"] = "redis://localhost:6379/0"
app.config["UP_DIR"]= os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/")#上传文件的目录
app.config["FC_DIR"]= os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/users/")#上传头像的目录
app.debug = True
db = SQLAlchemy(app)
rd = FlaskRedis(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint,url_prefix="/admin")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"),404