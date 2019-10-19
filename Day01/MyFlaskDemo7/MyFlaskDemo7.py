from flask import Flask, make_response, request, render_template, session,redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
#连接数据库
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:120913@localhost:3306/flask"
#自动提交数据库
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
#配置 SECRET_KEY
app.config['SECRET_KEY']='INPUT A STRING'

db=SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "users2"
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(50),nullable=False)
    upwd = db.Column(db.String(50),nullable=False)
    realname = db.Column(db.String(30),nullable=False)

    def __repr__(self):
        return "<Users %r>" % self.uname

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
   # username= request.cookies["username"]
   keywords=request.cookies['keywords']
   print('keywords:%s' % (keywords))
   return "get cookie ok"

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        # 判断之前是否有成功登录过(id和uname是否存在于cookie上)
        if 'id' in request.cookies and 'uname' in request.cookies:
            return "您已成功登录"
        else:
            # 去往 login.html 模板上
            return render_template('01_login.html')

    else:
        #1.接收用户名和密码
        uname = request.form.get('uname')
        upwd = request.form.get('upwd')
        #2.验证用户名和密码是否正确(数据库查询)
        user=Users.query.filter_by(uname=uname,upwd=upwd).first()
        if user:
            resp=make_response('登录成功')
            # 登录成功
            # 3.如果正确的话，判断是否记住密码
            if 'isSaved' in request.form:
                # 将　id 和　uname 保存进cookie
                m_age=60*60*24
                resp.set_cookie('id',str(user.id),max_age=m_age)
                resp.set_cookie('uname',uname,max_age=m_age)
            return resp
        else:
            #4.如果不正确的话，则给出提示
            return '登录失败'

#设置一个session
@app.route('/setSession')
def setSession():
    #1.向session中保存数据
    session['username']='sabfeng.zhang'
    return "Set session Success"

#得到对应的session值
@app.route('/getSession')
def getSession():
    username=session['username']
    return 'session值为：'+username

#删除一个session
@app.route('/delSession')
def delSession():
    del session['username']
    return "Delete Session Success"

#练习1
@app.route('/sign_in',methods=['GET','POST'])
def sign_in():
    if request.method=='GET':
        return render_template('02_sign_in.html')
    else:
        uname=request.form['uname']
        upwd=request.form['upwd']
        user=Users.query.filter_by(uname=uname,upwd=upwd).first()
        if user:
            #登录成功，将信息保存进　session
            session['id']=user.id
            session['uname']=user.uname
            #登录成功,跳转首页模板
            return redirect('/index')
        else:
            # 登录失败，回到sign_in.html
            return render_template('02_sign_in.html')
@app.route('/index')
def index():
    # 判断用户是否登录成功
    if 'id' in session and 'uname' in session:
        uname=session['uname']
    return render_template('02_index.html',params=locals())

@app.route('/sign_out')
def sign_out():
    if 'id' in session  and 'uname' in session:
        del session['id']
        del session['uname']
    return redirect('/index')

@app.route('/create_xhr')
def create_xhr():
    return render_template('03_xhr.html')


if __name__ == '__main__':
    app.run(debug=True)

