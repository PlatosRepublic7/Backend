import os
from flask import Flask, render_template, request
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

    from . import index
    app.register_blueprint(index.bp)

    from . import db

    # For getting raw query data -- FOR QUERY VALIDATION ONLY
    @app.route('/sqla')
    def sqlquery():
        r_list = []
        cnx = db.get_db()
        result = cnx.execute(text('SELECT title, description, release_year, length, rating FROM film WHERE film.title="CAT CONEHEADS"'))
        for row in result.mappings():
            r_list.append(row)
        db.close_db()
        return str(r_list)
    
    return app
