#主业务逻辑中的视图和路由的定义
from flask import render_template
#导入蓝图程序，用于构建路由
from . import main
#导入db，用于操作数据库
from .. import db
#导入实体类，用于操作数据库
from ..models import *

# 主页的访问路径
@main.route('/')
def main_index():
  #查询所有的Category的信息
  categories = Category.query.all()
  #查询所有的Topic的信息
  topics = Topic.query.all()
  return render_template('index.html',params = locals())

# 登录页面的访问路径
@main.route('/login')
def login_views():
  return render_template('login.html')

#　注册页面的访问路径
@main.route('/register')
def register_views():
  return render_template('register.html')

# 发表博客的访问路径
@main.route('/release')
def release_views():
  return render_template('release.html')








