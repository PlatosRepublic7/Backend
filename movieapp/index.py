import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from movieapp.db import get_db
from sqlalchemy import text

# Create blueprint for the index view
bp = Blueprint('index' ,__name__, url_prefix='/index')

# Create different routes for each of the pages, and define the functionality of each
@bp.route('/home', methods=('GET', 'POST'))
def home():
    db = get_db()
    # Queries for intial/updated form population
    top_movies = db.execute(text('SELECT film.title, COUNT(rental.return_date) AS "rented" FROM ((rental INNER JOIN inventory ON rental.inventory_id = inventory.inventory_id) INNER JOIN film ON inventory.film_id = film.film_id)'\
                                'WHERE rental.return_date IS NOT NULL GROUP BY film.title ORDER BY rented DESC LIMIT 5'))
    top_actors = db.execute(text('SELECT actor.actor_id, actor.first_name, actor.last_name, COUNT(*) AS "movies" FROM ((actor INNER JOIN film_actor ON actor.actor_id = film_actor.actor_id)'\
                                'INNER JOIN film ON film.film_id = film_actor.film_id) GROUP BY actor.actor_id ORDER BY movies DESC LIMIT 5'))
    
    # Handle form submissions
    if request.method == 'POST':
        if "movie" in request.form:
            movie = request.form['movie']
        
            movie_res = db.execute(text('SELECT title, description, release_year, length, rating FROM film WHERE film.title="{}"'.format(movie)))

            return render_template('index/home.html', posts=movie_res, tmovies = top_movies, tactors = top_actors)
        elif "actors" in request.form:
            actor = request.form['actors']
            name = actor.split()
            actor_res = db.execute(text('SELECT actor.first_name, actor.last_name, film.title, COUNT(rental.return_date) AS "rented" FROM ((((rental INNER JOIN inventory ON rental.inventory_id = inventory.inventory_id)'\
                                    'INNER JOIN film ON inventory.film_id = film.film_id) INNER JOIN film_actor ON film.film_id = film_actor.film_id)' \
                                    'INNER JOIN actor ON film_actor.actor_id = actor.actor_id) WHERE rental.return_date IS NOT NULL AND actor.first_name = "{}" AND actor.last_name = "{}"' \
                                    'GROUP BY film.title ORDER BY rented DESC LIMIT 5'.format(name[0], name[1])))
            return render_template('index/home.html', actors=actor_res, tmovies = top_movies, tactors = top_actors)
    else:
        return render_template('index/home.html', tmovies = top_movies, tactors = top_actors)


@bp.route('/movies', methods=('GET', 'POST'))
def movies():
    db = get_db()
    
    if request.method == 'GET':
        if request.args.get('titleq'):
            stext = request.args.get('titleq')
            db_res = db.execute(text('SELECT title FROM film WHERE film.title="{}"'.format(stext)))
            
            return render_template('index/movies.html', results=db_res, stitle = stext)

        elif request.args.get('actorq'):
            stext = request.args.get('actorq')
            slist = stext.split()
            db_res = db.execute(text('SELECT film.title FROM ((actor INNER JOIN film_actor ON actor.actor_id = film_actor.actor_id)'\
                                    'INNER JOIN film ON film_actor.film_id = film.film_id) WHERE actor.first_name = "{}" AND actor.last_name = "{}"'.format(slist[0], slist[1])))
            
            return render_template('index/movies.html', results=db_res, stitle = stext)
        
        elif request.args.get('genreq'):
            stext = request.args.get('genreq')
            db_res = db.execute(text('SELECT film.title, category.name AS "genre" FROM ((film_category INNER JOIN category ON film_category.category_id = category.category_id)' \
                                    'INNER JOIN film ON film.film_id = film_category.film_id) WHERE category.name = "{}"'.format(stext)))
            
            return render_template('index/movies.html', results=db_res, stitle = stext)
        
        else:            
            return render_template('index/movies.html')
    
    elif request.method == 'POST':
        if 'sresults' in request.form:
            movie = request.form['sresults']
            movie_res = db.execute(text('SELECT title, description, release_year, length, rating FROM film WHERE film.title="{}"'.format(movie)))

            return render_template('index/movies.html', fields = movie_res, film_title = movie)
        else:
            return render_template('index/movies.html')


@bp.route('/customers', methods=('GET', 'POST'))
def customers():
    db = get_db()
    customer_list = db.execute(text('SELECT customer.customer_id, customer.first_name, customer.last_name FROM customer'))

    return render_template('index/customers.html', customers = customer_list)
