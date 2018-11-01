
from exts import db

# class Detail(db.Model):
#     __tablename__ = 'Detail'
#     id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     Latitude = db.Column(db.String(100),nullable=False)
#     longitude = db.Column(db.String(100),nullable=False)

class Item(db.Model):
    __tablename__ = 'Item'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    table = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.String(400),nullable=False)
    # longitude = db.Column(db.String(100),nullable=False)