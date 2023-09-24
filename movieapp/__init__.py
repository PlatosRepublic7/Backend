import os
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from sqlalchemy import text


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'movieapp')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #app.config['MYSQL_HOST'] = 'localhost'
    #app.config['MYSQL_USER'] = 'rkitson'
    #app.config['MYSQL_PASSWORD'] = 'PlatosRepublic777'
    #app.config['MYSQL_DB'] = 'sakila'

    #mysql = MySQL(app)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    

    from . import db

    @app.route('/sqla')
    def sqlquery():
        r_list = []
        cnx = db.get_db()
        result = cnx.execute(text("SHOW TABLES"))
        for row in result.mappings():
            r_list.append(row)
        db.close_db()
        return str(r_list)


    @app.route('/query')
    def get_query():
        cursor = mysql.connection.cursor()
        cursor.execute('''SHOW TABLES''')
        rv = cursor.fetchall()
        cursor.close()
        return str(rv)


    @app.route('/connect')
    def connection():
        cnx = db.get_db()
        number = db.make_query(cnx)
        db.close_db()
        return number
    
    return app
