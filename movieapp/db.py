from flask import g
from sqlalchemy import create_engine
import click



def get_db():
    # Set up mysql connection to database
    if 'db' not in g:
        # UPDATE THIS LINE TO WORK WITH YOUR SAKILA DATABASE SERVER
        # The string should be in the format "mysql+mysqlconnector://{user_name}:{password}@{host_system}:{port}/sakila"
        # Other machine rkitson:PlatosRepublic777@localhost:3306/sakila
        engine = create_engine("mysql+mysqlconnector://root:Karamazov7789@localhost:3306/sakila")
        g.db = engine.connect()
        return g.db

        

# NOT USED (YET?)
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

def init_db():
    db = get_db()
    return db

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo("Connected to the Database")
