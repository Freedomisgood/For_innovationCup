from flask import Flask,request,render_template,redirect,url_for
import config
from exts import db
from models import *
import json
app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = dict(request.form)
        return '{}'.format(data),203

@app.route('/data/',methods=['GET','POST'])
def data():
    if request.method == 'GET':
        return render_template('data.html')
    else:
        if request.method == 'POST':
            json_data = request.form
            item = Item.query.filter(Item.table == json_data.get('table')).first()
            if item:
                return 'exist', 203
            else:
                item = Item(table=json_data.get('table'), detail=request.form.get('data'))
                db.session.add(item)
                db.session.commit()
                return 'Create',200



# @app.route('/add/<int:table>',methods=['GET','POST'])
# def add(table):
#     if request.method == 'POST':
#         item = Item.query.filter( Item.table == table ).first()
#         if item:
#             return 'exist',203
#         else:
#             table = request.form.get('table')
#             data = request.form.get('data')
#             item = Item(table = table, detail = data)
#             db.session.add(item)
#             db.session.commit()
#             return 'Create',200

@app.route('/query/<int:table>')
def query(table):
    item = Item.query.filter(Item.table == table).first()
    if item:
        data  = item.detail
        return '{}'.format(data),200
    else:
        return "fail",402

if __name__ == '__main__':
    app.run()
