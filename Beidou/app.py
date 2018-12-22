from flask import Flask,request,render_template,redirect,url_for,jsonify,json
from flask_mail import Message
import config
from exts import db,mail
from decorators import async
from models import *
import time
import os
import base64
import requests
from conv2d import ObstacleDetection

basedir = os.path.abspath(os.path.dirname(__file__))
TOKEN = ''
token_data = {
    'grant_type': 'client_credentials',
    'client_id': '1EXbMlBW9UojvgMIyMXcLtdD',
    'client_secret': '5A96ChlLj4hgMVuCdy1W6ph8M6sZ6ota'
}

app = Flask(__name__)
app.config.from_object(config)

mail.init_app(app)
db.init_app(app)

@async
def send_async_email(app,msg):
    with app.app_context():
       mail.send(message=msg)
       TOKEN = getToken()


def SendMail(content,toEmail):
    '''
    发送邮件
    :param content: 发送的内容
    :param toEmail: Email list
    :return:
    '''
    msg = Message('老人有情况!',sender= config.MAIL_USERNAME  ,recipients=toEmail)
    msg.body = content
    send_async_email(app, msg)
    return 'ok'


@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        name = request.form.get('UID')
        pwd = request.form.get('PWD')
        user = Account.query.filter(Account.Username == name).first()
        if user:
            if pwd != user.PWD:
                return '密码错误'
            else:
                return redirect('/map/{}'.format(name))
                # return redirect( url_for('show_map',num = name) )
        else:
            return "用户不存在,请注册"

@app.route('/signup/',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        data = request.form
        user = Account.query.filter(Account.Username ==  data.get('UID')).first()
        if user:
            return "账号已存在"
        try:
            userinfo =  Account(Username = data.get('UID') , PWD = data.get('PWD'),
                                email = data.get('email'))
            db.session.add(userinfo)
            db.session.commit()
        except:
            return  "注册失败"
        else:
            return "注册成功,你的账号是{},密码是{}".format(data.get('UID') ,data.get('PWD'))


@app.route('/map/<num>',methods=['GET','POST'])
def show_map(num):
    if request.method == 'GET':
        user = Account.query.filter(Account.Username == num).first()
        if user:
            ids = Info.query.filter(Info.email==user.email).count()
            lastItem = Info.query.filter(Info.id == ids).first()
            Points = []
            Markers = []
            if lastItem:
                for x in lastItem.tmps.all():
                    nowtime = time.localtime( x.nowtime )
                    timeArr = time.strftime("%H:%M:%S", nowtime)
                    Points.append( [x.nowtime,x.longitude,x.latitude] )
                    if x.fallen == 1:
                        Markers.append( [x.nowtime,x.longitude,x.latitude] )
            print(Points)
            print("Markers",Markers)
            return render_template('baidu.html',P = Points , M = Markers)
        else:return jsonify({"msg":"Error",'status':400})

    if request.method == 'POST':
        user = Account.query.filter(Account.Username == num).first()
        if user:
            #  处理表单信息
            post_data = request.form
            longitude = post_data.get('longitude')     # 经度
            latitude = post_data.get('latitude')
            fallen = 0

            if post_data.get('add') == '1': # 如果是创建一个新的记录
                timestamp = int( time.time() )
                info = Info( email= user.email ,timestamp = timestamp )
                db.session.add(info)  # 事务
                db.session.commit()  # 必须要提交
                return jsonify({"msg":"create",'status':200})

            if post_data.get('f') == '1': #如果摔倒,发送邮件
                nowtime = time.localtime( time.time() )
                timeArr = time.strftime("%Y-%m-%d %H:%M:%S", nowtime)
                SendMail('监护对象在{},位置{}°E,{}°N处摔倒.'.format(timeArr,
                        longitude,latitude),[user.email])
                fallen = 1
                # 增加marker

            if longitude and latitude:
                ids = Info.query.filter(Info.email == user.email).count()
                lastItem = Info.query.filter(Info.id == ids).first()
                searchTMP = lastItem.timestamp  # 通过info的timestamp的最后一条消息

                tmp = Tmp(timestamp=searchTMP , longitude = longitude ,
                          latitude = latitude,nowtime=int(time.time()) ,fallen = fallen)
                print(tmp.timestamp,tmp.longitude,tmp.latitude , tmp.nowtime )
                db.session.add(tmp)
                db.session.commit()

                img = request.files.get('src')
                if img:
                    path = basedir + "/static/img/"
                    file_path = path + 'tmp.png'
                    img.save(file_path)
                return jsonify({"msg":"update",'status':200})
            else: return "ERROR,longitude and latitude are NULLABLE",404
        else:return jsonify({"msg":"不存在该账户",'status':404})


@app.route('/pic/',methods = ['POST'])
def pic():
    global TOKEN
    if request.method == "POST":
        img = request.files.get('src')
        if img:
            file_path = basedir + '/static/img/tmp.png'
            img.save(file_path)
            msg = copePic()
            return jsonify({"msg":msg,'status':200})
        return jsonify({"msg":"No pic",'status':200})
    return jsonify({"msg":'Error','status':404})


def copePic():
    global TOKEN
    if not TOKEN:
        TOKEN = getToken()

    knowurl = "https://aip.baidubce.com/rest/2.0/face/v3/search?access_token=" + TOKEN
    with open(basedir + '/static/img/tmp.png', 'rb') as f:
        im = base64.b64encode(f.read())
        params = {"group_id_list": "Beidou",
                  "image": im,
                  "image_type":"BASE64"}
        html = requests.post(knowurl,data = params
                             ,headers={'Content-Type': 'application/json'})
        res = html.json()
        error_msg =res.get('error_msg')
        if error_msg == "SUCCESS":
            # print(res.get('result').get('user_list')[0].get('score'))
            return res.get('result').get('user_list')[0].get('user_id')
        elif error_msg == 'pic not has face':
            ob = ObstacleDetection()
            return ob.run(img_path=basedir+'/static/img/tmp.png')
        else: return 'None'


def getToken():
    html = requests.post('https://aip.baidubce.com/oauth/2.0/token',data = token_data)
    return html.json().get('access_token')


if __name__ == '__main__':
    app.run(debug=True)






