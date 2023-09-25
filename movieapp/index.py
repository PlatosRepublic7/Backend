import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from movieapp.db import get_db
from sqlalchemy import text

# Create blueprint for the index view
bp = Blueprint('index' ,__name__, url_prefix='/index')

# Create different routes for each of the pages, and define the functionality of each
@bp.route('/home', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        db = get_db()
        if "movie" in request.form:
            movie = request.form['movie']
        
            movie_res = db.execute(text('SELECT title, description, release_year, length, rating FROM film WHERE film.title="{}"'.format(movie)))

            return render_template('index/home.html', posts=movie_res)
        elif "actors" in request.form:
            actor = request.form['actors']
            name = actor.split()
            actor_res = db.execute(text('SELECT actor.first_name, actor.last_name, film.title, COUNT(rental.return_date) AS "rented" FROM ((((rental INNER JOIN inventory ON rental.inventory_id = inventory.inventory_id)'\
                                    'INNER JOIN film ON inventory.film_id = film.film_id) INNER JOIN film_actor ON film.film_id = film_actor.film_id)' \
                                    'INNER JOIN actor ON film_actor.actor_id = actor.actor_id) WHERE rental.return_date IS NOT NULL AND actor.first_name = "{}" AND actor.last_name = "{}"' \
                                    'GROUP BY film.title ORDER BY rented DESC LIMIT 5'.format(name[0], name[1])))
            return render_template('index/home.html', actors=actor_res)
    else:
        return render_template('index/home.html')

@bp.route('/movies', methods=('GET', 'POST'))
def movies():
    return render_template('index/movies.html')

@bp.route('/customers', methods=('GET', 'POST'))
def customers():
    return render_template('index/customers.html')
