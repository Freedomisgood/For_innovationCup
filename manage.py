from main import app
from flask_script import Manager
# from DB_script import DB_manager
from flask_migrate import Migrate,MigrateCommand
from models import *

manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

@manager.command
def init():
    db.create_all()

# manager.add_command('前缀',DB_manager)
if __name__ == '__main__':
    manager.run()