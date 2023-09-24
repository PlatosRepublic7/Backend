from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import click



def get_db():
    # Set up mysql connection to database
    if 'db' not in g:
        engine = create_engine("mysql+mysqlconnector://rkitson:PlatosRepublic777@localhost:3306/sakila")
        g.db = engine.connect()
        return g.db

        

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

def init_db():
    db = get_db()
    return db

def make_query(cnx):
    cursor = cnx.cursor()
    query = "SELECT COUNT(*) FROM film;"

    cursor.execute(query)
    for num in cursor:
        out_string = "Entries in film: {}".format(num)

    cursor.close()

    return out_string

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo("Connected to the Database")
