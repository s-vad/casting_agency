from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from models import db
from models import db, Movie, Actor

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    Movie(title='Spider Man', release_date='2018-01-01').insert()
    Movie(title='Iron Man', release_date='2018-01-01').insert()
    Movie(title='Thor', release_date='2018-01-01').insert()

    Actor(name='Robert Jr', age=45, gender='male').insert()
    Actor(name='Chris Evans', age=42, gender='male').insert()
    Actor(name='Elizabeth Olsen', age=38, gender='female').insert()


if __name__ == '__main__':
    manager.run()
