import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from movieapp.db import get_db
from sqlalchemy import text

# Create blueprint for the index view
bp = Blueprint('index' ,__name__, url_prefix='/index')

# Create different routes for each of the pages, and define the functionality of each
# Home/Landing Page
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


# Movies Page
@bp.route('/movies', methods=('GET', 'POST'))
def movies():
    db = get_db()
    
    # Search Field Handling
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
    
    # Results and Details Handling
    elif request.method == 'POST':
        if 'sresults' in request.form:
            movie = request.form['sresults']
            movie_res = db.execute(text('SELECT title, description, release_year, length, rating FROM film WHERE film.title="{}"'.format(movie)))

            return render_template('index/movies.html', fields = movie_res, film_title = movie)
        else:
            return render_template('index/movies.html')


# Customers Page
@bp.route('/customers', methods=('GET', 'POST'))
def customers():
    db = get_db()
    customer_list = db.execute(text('SELECT customer.customer_id, customer.first_name, customer.last_name FROM customer'))

    # Search Field and Customer List Population Handling
    if request.method == 'GET':
        
        if request.args.get('customerq'):
            stext = request.args.get('customerq')
            
            if stext is None:
                return render_template('index/customers.html', customers = customer_list)
            
            elif stext.isnumeric():
                db_search = db.execute(text('SELECT customer.customer_id, customer.first_name, customer.last_name FROM customer WHERE customer.customer_id = {}'.format(stext)))
                
            else:
                db_search = db.execute(text('SELECT customer.customer_id, customer.first_name, customer.last_name FROM customer WHERE '\
                                             'customer.first_name = "{}" OR customer.last_name = "{}"'.format(stext, stext)))

            return render_template('index/customers.html', customers = db_search)
    
    # Details Editing Form Handling
    elif request.method == 'POST':
        if 'clist' in request.form:
            customer = request.form['clist']
            clist = customer.split()
            c_res = db.execute(text('SELECT customer.store_id, customer.customer_id, customer.first_name, customer.last_name, customer.email, customer.active FROM customer' \
                                    ' WHERE customer.first_name = "{}" AND customer.last_name = "{}"'.format(clist[0], clist[1] )))

            return render_template('index/customers.html', c_details = c_res)
        if 'edit_form' in request.form:
            c_store_id = request.form['store_id']
            c_id = request.form['customer_id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            isactive = request.form['active']
            db.execute(text('UPDATE customer SET store_id = {}, first_name = {}, last_name = {}, email = {}, active = {} '\
                            'WHERE customer.customer_id = {}'.format(c_store_id, first_name, last_name, email, isactive, c_id)))
            db.commit()
            success_string = "Saved Customer Information"
            
            return render_template('index/customers.html', customers = customer_list, success = success_string)
        
    return render_template('index/customers.html', customers = customer_list)
