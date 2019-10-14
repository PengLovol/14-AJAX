from flask import Flask, make_response, request, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost:3306/flask"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SECRET_KEY'] = 'INPUT A STRING'
db=SQLAlchemy(app)

import pymysql
pymysql.install_as_MySQLdb()

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(50),nullable=False)
    upwd = db.Column(db.String(50),nullable=False)
    realname = db.Column(db.String(30),nullable=False)

    def __repr__(self):
        return "<Users %r>" % self.uname

# db.drop_all()
db.create_all()

@app.route('/set_cookie')
def set_cookie():
    # 将响应内容构建成响应对象
    resp = make_response("Set Cookie Success")
    # 保存数据进cookie
    resp.set_cookie('username','sf.zh')
    # 保存数据进cookie并设置max_age
    resp.set_cookie('keywords','Cannon',max_age=60*60*24*365)
    return resp


@app.route('/get_cookie')
def get_cookie():
    # username = request.cookies['username']
    keywords = request.cookies['keywords']
    print('keywords:%s' % (keywords))
    return "get cookie ok"

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        # 判断之前是否有成功登录过(id和uname是否存在于cookie上)
        if 'id' in request.cookies and 'uname' in request.cookies:
            return '您已成功登录'
        else:
            # 去往 login.html 模板上
            return render_template('login.html')
    else:
        # 1.接收用户名和密码
        uname = request.form['uname']
        upwd = request.form['upwd']
        # 2.验证用户名和密码是否正确(数据库查询)
        user = Users.query.filter_by(uname=uname,upwd=upwd).first()
        # 3.如果正确的话,判断是否记住密码
        if user:
            resp = make_response('登录成功')
            print(type(user.id))
            # 登录成功
            if 'isSaved' in request.form:
                # 将　id 和　uname 保存进cookie
                m_age = 60*60*24*365
                resp.set_cookie('id',str(user.id),max_age=m_age)
                resp.set_cookie('uname',uname,max_age=m_age)
            return resp
        else:
            # 4.如果不正确的话,则给出提示
            return "登录失败"
        pass

@app.route('/setSession')
def setSession():
    session['username'] = 'sanfeng.zhang'
    return "Set session Success"

@app.route('/getSession')
def getSession():
    username = session['username']
    return 'session值为:'+username

@app.route('/delSession')
def delSession():
    del session['username']
    return "Delete Session Success"

@app.route('/sign_in',methods=['GET','POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('sign_in.html')
    else:
        uname = request.form['uname']
        upwd = request.form['upwd']
        user = Users.query.filter_by(uname=uname,upwd=upwd).first()
        if user:
            # 登录成功，将信息保存进　session
            session['id'] = user.id
            session['uname'] = user.uname
            return redirect('/index')
        else:
            #　登录失败，回到sign_in.html
            return render_template('sign_in.html')

@app.route('/index')
def index():
    # 判断用户是否登录成功
    if 'id' in session and 'uname' in session:
        uname = session['uname']
    return render_template('index.html',params=locals())

@app.route('/sign_out')
def sign_out():
    if 'id' in session and 'uname' in session:
        del session['id']
        del session['uname']
    return redirect('/index')

@app.route('/create_xhr')
def create_xhr():
    return render_template('xhr.html')



if __name__ == '__main__':
    app.run(debug=True)
