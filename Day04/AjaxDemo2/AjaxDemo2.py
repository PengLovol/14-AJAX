from flask import Flask, render_template, request
import json
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:120913@localhost:3306/flask"
db = SQLAlchemy(app)

class Users(db.Model):
  __tablename__ = "users2"
  id = db.Column(db.Integer,primary_key=True)
  uname = db.Column(db.String(50))
  upwd = db.Column(db.String(50))
  realname = db.Column(db.String(30))

  # 将当前对象中的所有属性封装到一个字典中
  def to_dict(self):
    dic = {
      'id':self.id,
      'uname':self.uname,
      'upwd':self.upwd,
      'realname':self.realname
    }
    return dic


  def __repr__(self):
    return "<Users:%r>" % self.uname


class Province(db.Model):
  __tablename__ = "province"
  id = db.Column(db.Integer,primary_key=True)
  proname = db.Column(db.String(30),nullable=False)
  cities = db.relationship('City',backref='province',lazy='dynamic')

  def to_dict(self):
    dic = {
      'id' : self.id,
      'proname':self.proname
    }
    return dic

  def __init__(self,proname):
    self.proname = proname

  def __repr__(self):
    return "<Province:%r>" % self.proname

class City(db.Model):
  __tablename__ = "city"
  id = db.Column(db.Integer,primary_key=True)
  cityname = db.Column(db.String(30),nullable=False)
  pro_id = db.Column(db.Integer,db.ForeignKey("province.id"))

  def to_dict(self):
    dic = {
      'id' : self.id,
      'cityname' : self.cityname,
      'pro_id' : self.pro_id,
    }
    return dic

  def __init__(self,cityname,pro_id):
    self.cityname = cityname
    self.pro_id = pro_id

  def __repr__(self):
    return "<City:%r>" % self.cityname

db.create_all()


@app.route('/page')
def page_views():
  return render_template('01-page.html')

@app.route('/json')
def json_views():
  list = ["Fan Bingbing","Li Chen","Cui Yongyuan"]
  dic = {
    'name':'Bingbing Fan',
    'age' : 40,
    'gender':'female',
  }

  uList = [
    {
      'name': 'Bingbing Fan',
      'age': 40,
      'gender': 'female',
    },
    {
      'name' : "Jinbao Hong",
      'age' : 70,
      'gender' : 'male'
    }
  ]
  jsonStr = json.dumps(uList)
  return jsonStr

@app.route('/json_users')
def json_users():
  user = Users.query.filter_by(id=1).all()
  list = []
  for u in user:
    list.append(u.to_dict())
  return json.dumps(list)


@app.route('/01-users')
def users_01():
  return render_template('01-users.html')

@app.route('/01-server')
def server_01():
  users = Users.query.all()
  list = []
  for user in users:
    list.append(user.to_dict())
  return json.dumps(list)

@app.route('/02-province')
def province_views():
  return render_template('02-province.html')

@app.route('/02-loadPro')
def loadPro_views():
  provinces = Province.query.all()
  list = []
  for pro in provinces:
    list.append(pro.to_dict())
  return json.dumps(list)

@app.route('/02-loadCity')
def loadCity_views():
  # 接收前端传递过来的数据,pid为前端传递过来的参数名
  pid = request.args.get('pid')
  cities = City.query.filter_by(pro_id=pid).all()
  list = []
  for city in cities:
    list.append(city.to_dict())
  return json.dumps(list)

@app.route('/03-load')
def load_views():
  return render_template('03-load.html')

@app.route('/03-server',methods=['POST'])
def server_03():
  name = request.form.get('name')
  age = request.form.get('age')
  return "姓名:%s,年龄:%s" % (name,age)

@app.route('/04-get')
def get_views():
  return render_template('04-get.html')

@app.route('/04-server')
def server_04():
  cities = City.query.all()
  list = []
  for city in cities:
    list.append(city.to_dict())
  return json.dumps(list)

######### 10.09########
@app.route("/05-server")
def server_05():
  uname = request.args.get('uname')
  u = Users.query.filter_by(uname=uname).first()
  if u :
    return json.dumps(u.to_dict())
  else:
    dic = {
      'status' : "0",
      'msg' : '查找的用户不存在'
    }
    return json.dumps(dic)


@app.route('/06-server')
def server_06():
  # 接收前端传递过来的callback即前端处理响应数据的函数名
  cb = request.args.get('callback')
  #响应数据，被前端页面当成JS脚本被执行
  return cb+"('这是server_06响应回来的数据')"

@app.route('/07-server')
def server_07():
  cb = request.args.get('callback')
  dic = {
    'flightNO':'MU763',
    'from':'Beijing',
    'to':'Saipan',
    'time':'16:55'
  }
  # flight({'flightNO':'MU763'...})
  return cb+"("+json.dumps(dic)+")"


if __name__ == '__main__':
  app.run(debug=True)
