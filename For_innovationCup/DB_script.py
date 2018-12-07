from flask_script import Manager

DB_manager = Manager()


@DB_manager.command
def init():
    print('初始化')