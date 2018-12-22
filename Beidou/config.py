DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'cl123123'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'beidou'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
    DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False


MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
# 注意此处，很多人配置发不出去和这个是有关系的
MAIL_PASSWORD = 'zplpckduqktybbcg'
MAIL_USERNAME = '1063052964@qq.com'