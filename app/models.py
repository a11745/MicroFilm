#coding:utf8
from datetime import datetime

from werkzeug.security import generate_password_hash

from  app import  db

#会员数据模型
class User(db.Model):
    __tablename__ = "user"   #表名
    #__table_args__ = {"useexisting": True}
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True)#长度100  唯一
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100),unique=True)
    phone = db.Column(db.String(11),unique=True)
    info = db.Column(db.Text)#个性简介
    face = db.Column(db.String(255),unique=True)#头像
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)#添加索引
    uuid = db.Column(db.String(255),unique=True)#唯一标识符
    userlogs = db.relationship('Userlog',backref='user')#会员日志外键关系关联
    comments = db.relationship('Comment', backref='user')
    moviecols = db.relationship('Moviecol', backref='user')
    def __repr__(self): #定义返回类型
        return "<User %r>" % self.name
    def check_pwd(self,pwd):
        from  werkzeug.security import check_password_hash
        return check_password_hash(self.pwd,pwd)
#会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    #__table_args__ = {"useexisting": True}
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) #外键
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)#加入索引
    def __repr__(self): #定义返回类型
        return "<Userlog %r>" % self.id
#定义标签
class Tag(db.Model):
    __tablename__="tag"
    #__table_args__ = {"useexisting": True}
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True)
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)
    movies = db.relationship("Movie",backref='tag')#电影外键关联

    def __repr__(self):
        return "<Tag %r>"% self.name
#电影
class Movie(db.Model):
    __tablename__ = "movie"
    #__table_args__ = {"useexisting": True}
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255),unique=True)
    url = db.Column(db.String(255),unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255),unique=True)
    star = db.Column(db.SmallInteger)#星级 小整形
    playnum = db.Column(db.BigInteger)#播放量
    commentnum = db.Column(db.BigInteger)#评论量
    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id'))#所属标签
    area = db.Column(db.String(255))#上映地区
    release_time = db.Column(db.Date)#上映时间
    length = db.Column(db.String(100))#播放时间
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)
    comments = db.relationship('Comment', backref='movie')
    moviecols = db.relationship('Moviecol', backref='movie')

    def __repr__(self):
        return "<Movie %r>" % self.title
#上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    #__table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255),unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Preview %r>" % self.title
#电影评论
class Comment(db.Model):
    __tablename__ = "comment"
    #__table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Comment %r>" % self.id

#电影收藏
class Moviecol(db.Model):
    __tablename__="moviecol"
    #__table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Moviecol %r>" % self.id

#权限
class Auth(db.Model):
    __tablename__ = "auth"
   # __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Auth %r>" % self.name
#角色
class Role(db.Model):
    __tablename__ = "role"
    #__table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    admins = db.relationship("Admin", backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name

#管理员
class Admin(db.Model):
    __tablename__ = "admin"  # 表名
    #__table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)#是否为超级管理员  0为是
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    adminlogs = db.relationship("Adminlog",backref='admin')
    oplogs = db.relationship("Oplog", backref='admin')


    def __repr__(self):
        return "<Role %r>" % self.name
    def check_pwd(self,pwd):
        from  werkzeug.security import check_password_hash
        return check_password_hash(self.pwd,pwd)

#登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    #__table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 外键
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 加入索引

    def __repr__(self):  # 定义返回类型
        return "<Adminlog %r>" % self.id
#操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    #__table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 外键
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))#操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 加入索引

    def __repr__(self):  # 定义返回类型
        return "<Oplog %r>" % self.id

if __name__ == '__main__':
    #db.create_all()#用于运行生成表
    '''
    role = Role(
        name = "超级管理员",
        auths = ""
    )
    db.session.add(role)#添加内容
    db.session.commit()#需要提交才能生效
    '''
'''
    admin = Admin(
        name = "admin",
        pwd = generate_password_hash("admin"),#密码加密
        is_super = 0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()
'''



