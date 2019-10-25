#主业务逻辑中的视图和路由的定义
import datetime,os
from flask import render_template, request, session, redirect
#导入蓝图程序，用于构建路由
from . import main
#导入db，用于操作数据库
from .. import db
#导入实体类，用于操作数据库
from ..models import *
import json

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
        # 留言id
        gbook_id =user.ID

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
@main.route('/register',methods=['GET','POST'])
def register_views():
    if request.method=='GET':
        return render_template('register.html')
    else:
        #获取文本框的值并赋值给user实体对象
        user=User()
        user.loginname=request.form.get('loginname')
        user.uname=request.form.get('username')
        user.email=request.form.get('email')
        user.url=request.form.get('url')
        user.upwd=request.form.get('password')
        #将数据保存进数据库-注册
        db.session.add(user)
        #手动提交 ，目的是为了获取提交后的user的id
        db.session.commit()
        #当user成功插入进数据库之后，程序会自动将所有信息取出来再赋值给user
        uid=user.ID
        uname=user.uname
        #将登录信息保存进session，并完成登录操作
        session['uid']=uid
        session['uname']=uname
        return redirect('/')




#发表博客的访问路径
@main.route('/release',methods=['GET','POST'])
def release_views():
    if request.method=='GET':
        # 权限验证：验证用户是否有发表博客的权限即必须是登录用户并且is_author的值必须为1
        if 'uid' not in session or 'uname' not in session:
            return redirect('/login')
        else:
            user=User.query.filter_by(ID=session.get('uid')).first()
            #判断是否有权限登录
            if user.is_author!=1:
                return redirect('/')
        #有权限登录
        #查询category和blogtype
        categories=Category.query.all()
        blogTypes=BlogType.query.all()
        return render_template('release.html',params=locals())
    else:
        #处理post请求即发表博客的处理
        topic=Topic()
        # 为title赋值
        topic.title = request.form.get('author')
        # 为pub_date赋值
        topic.pub_date = datetime.datetime.now().strftime("%Y-%m-%d")
        # 为blogtype_id赋值
        topic.blogtype_id=request.form.get('list')
        # 为category_id赋值
        topic.category_id=request.form.get('category')
        # 为user_id赋值
        topic.user_id=session.get('uid')
        # 为content赋值
        topic.content=request.form.get('content')

        # 选择性的为 images 赋值
        if request.files:
            print('有文件上传')
            #取出文件
            f=request.files['picture']
            #处理文件名称，将名称赋值给topic.images
            #获取当前时间，作文文件名
            ftime=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            #获取文件扩展名
            ext=f.filename.split('.')[1]
            filename=ftime+"."+ext
            topic.images='upload/'+filename
            print('文件名：'+filename)
            #将文件保存至服务器
            basedir = os.path.dirname(os.path.dirname(__file__))
            upload_path = os.path.join(basedir, 'static/upload', filename)
            print(upload_path)
            f.save(upload_path)
        # #测试
        # print("%s,%s,%s,%s,%s,%s" % (topic.title, topic.blogtype_id, topic.category_id, topic.user_id, topic.content, topic.pub_date))
        db.session.add(topic)
        return redirect('/')

#退出的访问路径
@main.route('/logout')
def logout_views():
    if 'uid' in session and 'uname' in session:
        del session['uid']
        del session['uname']
    return redirect('/')

#表单验证:验证登录名是否重复
@main.route('/vertify_loginname')
def sever_vertify_loginname():
    loginname=request.args.get('loginname')
    user=User.query.filter_by(loginname=loginname).first()
    print(loginname)
    if user:
        resp='N'
    else:
        resp='Y'
    return resp

@main.route('/info',methods=['GET','POST'])
def info_views():
    if request.method=='GET':
        #完善静态网页：
        #查询
        categories=Category.query.all()
        #查询要看的博客信
        topic_id=request.args.get('topic_id')
        topic=Topic.query.filter_by(id=topic_id).first()
        #更新阅读量
        topic.read_num=int(topic.read_num)+1
        #查找上一篇 以及 下一篇
        # 上一篇：查询topic_id比当前topic_id值小的最后一条数据
        prevTopic=Topic.query.filter(Topic.user_id==topic.user_id,Topic.id<topic_id).order_by('id desc').first()
        # print("上一篇："+prevTopic.title)
        # 下一篇:查询topic_id比当前topic_id值大的第一条数据
        nextTopic = Topic.query.filter(Topic.user_id == topic.user_id, Topic.id > topic_id).first()
        # print("下一篇:" + nextTopic.title)
        # 查询登录用户
        if 'uid' in session and 'uname' in session:
            blog_uname = session.get('uname')
            blog_uid=int(session['uid'])
            user = User.query.filter_by(ID=blog_uid).first()
        return render_template('info.html',params=locals())

#添加留言功能
@main.route('/gbook',methods=['GET','POST'])
def gbook_views():
    if request.method=='GET':
        topic_id=request.args.get('topic_id')
        topic=Topic.query.filter_by(id=topic_id).first()
        #查询留言者的信息
        gbook=topic
        #读取repaaly中内容
        replies=topic.replies
        for reply in replies:
            print(reply.content)
        #查询博客category信息
        categories=Category.query.all()
        # 查询登录用户
        if 'uid' in session and 'uname' in session:
            login_uname = session.get('uname')
            login_uid=int(session['uid'])
            user = User.query.filter_by(ID=login_uid).first()
            print(login_uname,user.uname)
        return render_template('gbook.html',params=locals())
    else:
        #读取留言内容
        reply=Reply()
        topic_id=request.form.get('topic_id')
        reply.topic_id=request.form.get('topic_id')
        reply.user_id = request.form.get('user_id')
        reply.reply_time=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        reply.content=request.form.get('content')
        db.session.add(reply)
        db.session.commit()
        return redirect('/gbook?topic_id='+topic_id)