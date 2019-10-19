from flask import Flask, render_template, request
import pymysql
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost:3306/flask"
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(50))
    upwd = db.Column(db.String(50))
    realname =db.Column(db.String(30))



@app.route('/01-getxhr')
def getxhr():
    return render_template('01-getxhr.html')

@app.route('/02-get')
def get_views():
    return render_template('02-get.html')

@app.route('/02-server')
def server02_views():
    return "这是AJAX的请求"

@app.route('/03-get')
def get03_views():
    return render_template('03-get.html')

@app.route('/03-server')
def server03_views():
    uname = request.args['uname']
    return "欢迎:"+uname

@app.route('/04-post')
def post_views():
    return render_template('04-post.html')

@app.route('/04-server',methods=['POST'])
def server04_views():
    uname = request.form['uname']
    age = request.form['age']
    return "姓名:%s,年龄:%s" % (uname,age)

@app.route('/05-post')
def post05_views():
    return render_template('05-post.html')

@app.route('/06-checkname')
def checkname():
    return render_template('06-checkname.html')

@app.route('/06-server',methods=['POST'])
def server06_views():
    uname=request.form['username']
    user = Users.query.filter_by(uname=uname).first()
    if user:
        return "用户名称已存在"
    else:
        return "通过"


if __name__ == '__main__':
    app.run(debug=True)
