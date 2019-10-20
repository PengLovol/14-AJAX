from flask import Flask, render_template,request
import json
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:120913@localhost:3306/flask"
#指定执行完操作之后自动提交 ==db.session.commit()
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
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
          'id': self.id,
          'uname': self.uname,
          'upwd': self.upwd,
          'realname': self.realname
      }
      return dic
  def __repr__(self):
      return "<Users:%r>" % self.uname

class Province(db.Model):
     __tablename__="province"
     id=db.Column(db.Integer,primary_key=True)
     proname=db.Column(db.String(30),nullable=False)
     cities=db.relationship('City',backref='province',lazy='dynamic')
     def to_dict(self):
         dic={
             'id':self.id,
             'proname':self.proname
         }
         return dic
     def __init__(self,proname):
         self.proname=proname
     def __repr__(self):
         return "<Province:%r>"% self.proname

class City(db.Model):
    __tablename__="city"
    id=db.Column(db.Integer,primary_key=True)
    cityname=db.Column(db.String(30),nullable=False)
    pro_id=db.Column(db.Integer,db.ForeignKey("province.id"))
    def to_dict(self):
        dic={
            'id':self.id,
            'cityname':self.cityname,
            'pro_id':self.pro_id
        }
        return dic

    def __init__(self,cityname,pro_id):
        self.cityname=cityname
        self.pro_id=pro_id
    def __repr__(self):
        return "<City:%r>" % self.proname


db.create_all()


@app.route('/page')
def page_views():
  return render_template('01_page.html')

@app.route('/json')
def json_views():
    list = ["Fan Bingbing", "Li Chen", "Cui Yongyuan"]
    dic = {
        'name': 'Bingbing Fan',
        'age': 40,
        'gender': 'female',
    }

    uList = [
        {
            'name': 'Bingbing Fan',
            'age': 40,
            'gender': 'female',
        },
        {
            'name': "Jinbao Hong",
            'age': 70,
            'gender': 'male'
        }
    ]
    jsonStr=json.dumps(uList)
    return jsonStr

#将数据库中的一条记录此先存入字典中然后再转换为json对象
@app.route('/json_users')
def json_users():
    user = Users.query.filter_by(id=1).first()
    print(user)
    return json.dumps(user.to_dict())
# user = Users.query.filter_by(id=1).all(),#AttributeError: 'list' object has no attribute 'to_dict'
#将列表分解成字典，然后再调用to_dict方法
@app.route('/json_users_list')
def json_users_list():
    user = Users.query.all()
    print(user)
    list=[]
    for u in user:
        list.append(u.to_dict())
    return json.dumps(list)

#练习1

@app.route('/01_users')
def users_01():
    return render_template('01_users.html')

@app.route('/01_server')
def server_01():
   user=Users.query.all()
   list=[]
   for u in user:
       list.append(u.to_dict())
   return json.dumps(list)

#练习项目：省事级联操作
#向数据库中插入数据：省份和对应的城市
@app.route('/insert_province_city',methods=['GET','POST'])
def insert_province_city():
    if request.method=='GET':
        provinces=Province.query.all()
        cities=City.query.all()
        return render_template('02_insertDatabase.html',params=locals())
    else:
        proname=request.form['proname']
        cityname=request.form['cityname']
        provinceNew=Province(proname)

        #检查省份是否存入数据库中
        provinceQuery=Province.query.filter_by(proname=proname).first()
        if not provinceQuery:
            db.session.add(provinceNew)
        provinceQuery = Province.query.filter_by(proname=proname).first()
        pro_id = provinceQuery.id
        cityNew = City(cityname, pro_id)
        cityQuery=City.query.filter_by(cityname=cityname).first()
        if not cityQuery:
            db.session.add(cityNew)
        else:
            print("城市已存在")
        return "ok"

@app.route('/02_province')
def province_views():
    return render_template('02_province.html')

#从后端读取数据库中数据
@app.route('/02_loadPro')
def loadPro_views():
    provinces=Province.query.all()
    list=[]
    #将数据库中的查询结果存入列表中，最后将其转换为json格式的字符串，以便传给前端ajax处理
    for pro in provinces:
         list.append(pro.to_dict())
    return json.dumps(list)

@app.route('/02_loadCity')
def loadCit_views():
    #接收前端传递过来的函数,pid为前端传递过来的参数名
    pid=request.args.get('pid')
    cities=City.query.filter_by(pro_id=pid).all()
    list=[]
    for city in cities:
        list.append(city.to_dict())
    return json.dumps(list)

#JQUERY AJAX
@app.route('/03_load')
def load_views():
  return render_template('03_load.html')

@app.route('/03_server',methods=['POST'])
def server_03():
  name = request.form.get('name')
  age = request.form.get('age')
  return "姓名:%s,年龄:%s" % (name,age)


@app.route('/04_get')
def get_views():
  return render_template('04_get.html')

@app.route('/04_server')
def server_04():
  cities = City.query.all()
  list = []
  #响应字符串
  # return "使用jquery中的get方法请求的结果"

  #响应json对象
  for city in cities:
    list.append(city.to_dict())
  return json.dumps(list)

######-----------Day06###################
@app.route("/05_server")
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


#练习项目：更改省事级联操作：用$.ajax()完成
@app.route('/02_province_ajax')
def province_views_ajax():
    return render_template('02_province_ajax.html')

#从后端读取数据库中数据
@app.route('/02_loadPro_ajax')
def loadPro_views_ajax():
    provinces=Province.query.all()
    list=[]
    #将数据库中的查询结果存入列表中，最后将其转换为json格式的字符串，以便传给前端ajax处理
    for pro in provinces:
         list.append(pro.to_dict())
    return json.dumps(list)

@app.route('/02_loadCity_ajax')
def loadCit_views_ajax():
    #接收前端传递过来的函数,pid为前端传递过来的参数名
    pid=request.args.get('pid')
    cities=City.query.filter_by(pro_id=pid).all()
    list=[]
    for city in cities:
        list.append(city.to_dict())
    print(pid)
    return json.dumps(list)

#跨域
@app.route('/06_server')
def server_06():
  # 接收前端传递过来的callback即前端处理响应数据的函数名
  cb = request.args.get('callback')
  print(cb)
  #响应数据，被前端页面当成JS脚本被执行
  # return "show('这是server_06响应回来的数据')"
  return cb+"('这是server_06响应回来的数据')"


#练习2
@app.route('/07_server')
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




