#主业务逻辑中的视图和路由的定义
from flask import render_template, request, session, redirect
#导入蓝图程序，用于构建路由
from . import main
#导入db，用于操作数据库
from .. import db
#导入实体类，用于操作数据库
from ..models import *

#测试
@main.route('/test')
def test():
    #查找id为1的user的信息
    user=User.query.filter_by(ID=1).first()
    print(user.uname)
    topics=user.topics.all()
    for topic in topics:
        print(topic.title+":"+topic.user.uname+":"+topic.category.cate_name+":"+topic.blogtype.type_name)
    return 'OK'

#主页的访问路径
@main.route('/')
def main_index():
    # 查询所有的Category的信息
    categories=Category.query.all()
    #查询所有的Topic信息
    topics=Topic.query.all()
    #获取登录信息
    if 'uid' in session and 'uname' in session:
        user=User.query.filter_by(ID=session.get('uid')).first()
    return render_template('index.html',params=locals())

#登录页面的访问路径
@main.route('/login',methods=['GET','POST'])
def login_views():
    #直接输入/login的情况
    if 'uid' in session and 'uname' in session:
        return redirect('/')
    else:
        if request.method=='GET':
            return render_template('login.html')
        else:
            #接收前端传过来的数据
            loginname=request.form.get('username')
            upwd=request.form.get('password')
            #使用接收的用户名和密码到数据库中查询
            user=User.query.filter_by(loginname=loginname,upwd=upwd).first()
            #如果用户存在，将信息保存进session并重定向回首页，否则重定向回登录页
            if user:
                session['uid']=user.ID
                session['uname']=user.uname
                return redirect('/')
            else:
                errMsg="用户名或密码不正确"
                return render_template('login.html',errMsg=errMsg)

#注册页面的访问路径
@main.route('/register')
def register_views():
    return render_template('register.html')

#发表博客的访问路径
@main.route('/release')
def release_views():
    return render_template('release.html')

#退出的访问路径
@main.route('/logout')
def logout_views():
    if 'uid' in session and 'uname' in session:
        del session['uid']
        del session['uname']
    return redirect('/')