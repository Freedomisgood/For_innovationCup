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
            print(json_data)
            item = Item.query.filter(Item.table == json_data.get('table')).first()
            if item:
                return 'exist', 203
            else:
                #{"1":{"id":1,"num":2,"cost":45},"2":{"id":2,"num":3,"cost":26}}
                detail_dict =  json.loads(json_data.get('detail'))
                recipeList = [x for x in detail_dict.values()]
                List2str =  json.dumps(recipeList)
                item = Item(table=json_data.get('table'), detail=List2str)
                db.session.add(item)
                db.session.commit()
                return 'Create',200



@app.route('/delete/',methods=['GET','POST'])
def delete():
    if request.method == 'GET':
        return 'please use method POST',203
    if request.method =='POST':
        table = request.form.get('table')
        item = Item.query.filter(Item.table == table).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return 'Delete',200
        else:
            return "Don't exist",402



@app.route('/query/<int:table>/')
def query(table):
    item = Item.query.filter(Item.table == table).first()
    if item:
        data  = item.detail
        return '{}'.format(data),200
    else:
        return "fail",402

if __name__ == '__main__':
    app.run(debug=True)

