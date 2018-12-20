from exts import db
import time


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    Username = db.Column(db.String(30),nullable=True,unique=True)
    PWD = db.Column(db.String(20),nullable=True)
    email = db.Column(db.String(25),nullable=True,unique=True)


class Info(db.Model):
    __tablename__ = 'info'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(25),db.ForeignKey('account.email'))
    timestamp = db.Column(db.Integer,nullable=True,unique=True,default=int(time.time()))
    tmps = db.relationship('Tmp',backref= 'Info' ,lazy='dynamic')



class Tmp(db.Model):
    __tablename__ = 'tmp'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    timestamp = db.Column(db.Integer,db.ForeignKey('info.timestamp') )    # 一组的开始时间
    # timestamp = db.Column(db.Integer,db.ForeignKey('info.timestamp'),default=int(time.time()) )    # 一组的开始时间
    nowtime = db.Column(db.Integer,nullable=True )       # 当前记录的时间
    longitude = db.Column(db.Float,nullable=True)
    latitude = db.Column(db.Float,nullable=True)
    fallen = db.Column(db.Integer,default=0)



