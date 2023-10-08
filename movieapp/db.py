from flask import g
from sqlalchemy import create_engine
import click


# Parse and extract info from credentials.cfg file for database connection
def get_credentials():
    config = {'user_name': '', 'password': '', 'host_system': '', 'port': ''}
    with open("credentials.cfg", "r") as c_file:
        line_list = []
        for line in c_file.readlines():
            info = line.split()
            line_list.append(info[1])
        c_file.close()

    config['user_name'] = line_list[0]
    config['password'] = line_list[1]
    config['host_system'] = line_list[2]
    config['port'] = line_list[3]
    
    return config


def get_db():
    # Set up mysql connection to database
    if 'db' not in g:
        credentials = get_credentials()
        engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/sakila".format(credentials['user_name'], credentials['password'], credentials['host_system'], credentials['port']))
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
