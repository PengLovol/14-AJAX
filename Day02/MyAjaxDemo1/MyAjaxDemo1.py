from flask import Flask, render_template,request
import pymysql
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:120913@localhost:3306/flask"
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "users2"
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(50))
    upwd = db.Column(db.String(50))
    realname =db.Column(db.String(30))
    def __init__(self,uname,upwd,realname):
        uname=self.uname
        upwd=self.upwd
        realname=self.realname




@app.route('/01_getxhr')
def getxhr():
    return render_template('01_getxhr.html')

@app.route('/02_get')
def get_views():
    return render_template('02_get.html')

@app.route('/02_server')
def server02_views():
    return "这是AJAX的请求"

#练习1
@app.route('/03_get')
def get03_views():
    return render_template('03_get.html')
@app.route('/03_server')
def server03_views():
    uname=request.args['uname']
    return "欢迎："+uname

@app.route('/04_post')
def post_views():
    return render_template('04_post.html')

@app.route('/04_server',methods=['POST'])
def server04_views():
    uname = request.form['uname']
    age = request.form['age']
    return "姓名:%s,年龄:%s" % (uname,age)

@app.route('/05_post')
def post05_views():
    return render_template('05_post.html')

#练习3
@app.route('/06_checkname')
def checkname():
    return render_template('06_checkname.html')

@app.route('/06_server',methods=['POST'])
def server06_views():
    uname=request.form['username']
    user = Users.query.filter_by(uname=uname).first()
    if user:
        return "用户名称已存在"
    else:
        return "通过"

if __name__ == '__main__':
    app.run(debug=True)
