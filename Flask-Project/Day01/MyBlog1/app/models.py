#与当前项目相关的模型文件，即所有的实体类在此编写
from . import db

#创建category表的实体类
class Category(db.Model):
    __tablename__='category'
    id=db.Column(db.Integer,primary_key=True)
    cate_name=db.Column(db.String(50),nullable=False)
    #增加与Topci之间的关联关系以及反向引用
    topics=db.relationship('Topic',backref='category',lazy="dynamic")


#创建blogtype表的实体类
class BlogType(db.Model):
    __tablename__='blogtype'
    id=db.Column(db.Integer,primary_key=True)
    type_name=db.Column(db.String(20),nullable=False)
    #增加与Topcic之间的关联关系以及反向引用
    topics=db.relationship('Topic',backref='blogtype',lazy='dynamic')


#创建user表的实体类
class User(db.Model):
    __tablename__='user'
    ID=db.Column(db.Integer,primary_key=True)
    loginname=db.Column(db.String(50),nullable=False)
    uname=db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(200), nullable=False)
    url= db.Column(db.String(200))
    upwd = db.Column(db.String(30), nullable=False)
    is_author=db.Column(db.SmallInteger,default=0)
    #增加与Topcic之间的关联关系以及反向引用
    topics=db.relationship('Topic',backref='user',lazy='dynamic')
    #增加与Replay之间的关联关系以及反向引用
    replies=db.relationship('Reply',backref='user',lazy='dynamic')

    #增加与Topic之间的关联关系以及反向引用(多对多)
    #voke_topics表示点赞数
    voke_topics=db.relationship('Topic',
                                secondary='voke',
                                backref=db.backref('voke_users',lazy='dynamic'),
                                lazy='dynamic')




#创topic表的实体类
class Topic(db.Model):
  __tablename__ = "topic"
  id = db.Column(db.Integer,primary_key=True)
  title = db.Column(db.String(200),nullable=False)
  pub_date = db.Column(db.DateTime,nullable=False)
  read_num = db.Column(db.Integer,default=0)
  content = db.Column(db.Text,nullable=False)
  images = db.Column(db.Text)
  #关系：一(Category)对多(Topic)的关系
  category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
  #关系：一(BlogType)对多(Topic)的关系
  blogtype_id=db.Column(db.Integer,db.ForeignKey('blogtype.id'))
  #关系：一(User)对多(Topic)的关系
  user_id=db.Column(db.Integer,db.ForeignKey('user.ID'))

  #增加与Replay之间的关联关系以及反向引用
  replies=db.relationship('Reply',backref='topic',lazy='dynamic')

# 创reply表的实体类
class Reply(db.Model):
  __tablename__ = 'reply'
  id = db.Column(db.Integer,primary_key=True)
  content = db.Column(db.Text,nullable=False)
  reply_time = db.Column(db.DateTime)
  #关系：一(User)对多(Replay)的关系
  topic_id=db.Column(db.Integer,db.ForeignKey('topic.id'))
  # 关系：一(User)对多(Reply)的关系
  user_id=db.Column(db.Integer,db.ForeignKey('user.ID'))

#创建user和topic多对多的关联表
Voke=db.Table(
    'voke',
    db.Column('id',db.Integer,primary_key=True),
    db.Column('user_id',db.Integer,db.ForeignKey('user.ID')),
    db.Column('topic_id',db.Integer,db.ForeignKey('topic.id'))
)