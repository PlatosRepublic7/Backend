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

    # For getting raw query data -- FOR TESTING ONLY
    @app.route('/sqla')
    def sqlquery():
        r_list = []
        cnx = db.get_db()
        result = cnx.execute(text('SELECT actor.first_name, actor.last_name, film.title, COUNT(rental.return_date) AS "rented" FROM ((((rental INNER JOIN inventory ON rental.inventory_id = inventory.inventory_id) INNER JOIN film ON inventory.film_id = film.film_id) INNER JOIN film_actor ON film.film_id = film_actor.film_id) INNER JOIN actor ON film_actor.actor_id = actor.actor_id) WHERE rental.return_date IS NOT NULL AND actor.first_name = "GINA" AND actor.last_name = "DEGENERES" GROUP BY film.title ORDER BY rented DESC LIMIT 5'))
        for row in result.mappings():
            r_list.append(row)
        db.close_db()
        return str(r_list)
    
    return app
