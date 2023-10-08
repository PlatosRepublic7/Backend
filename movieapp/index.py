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

        # Collect GET request arguments and classify where it came from
        request_keys = []
        is_cust_search = False
        is_add_cust = False 
        for k, v in request.args.items():
            request_keys.append({k: v})
            if k == 'customerq':
                is_cust_search = True
            elif k == 'add_cust':
                is_add_cust = True

        # Perform add customer request logic, passes queried information to pre-populate and display the add_cust form
        if is_add_cust:
            # Get the largest (newest) customer ID from the database
            db_count = db.execute(text('SELECT customer.customer_id FROM customer ORDER BY customer.customer_id DESC LIMIT 1'))
            # flash is for request verification (REMOVE BEFORE DONE)
            flash(request_keys)
            
            return render_template('index/customers.html', add_cust = is_add_cust, db_count = db_count, customers = customer_list)
        
        # Perform customer search logic
        if is_cust_search:
            stext = request.args.get('customerq')
            
            flash(request_keys)
            
            if stext == "":
                return render_template('index/customers.html', customers = customer_list)
            
            elif stext.isnumeric():
                db_search = db.execute(text('SELECT customer.customer_id, customer.first_name, customer.last_name FROM customer WHERE customer.customer_id = {}'.format(stext)))
                
            else:
                db_search = db.execute(text('SELECT customer.customer_id, customer.first_name, customer.last_name FROM customer WHERE '\
                                             'customer.first_name = "{}" OR customer.last_name = "{}"'.format(stext, stext)))

            return render_template('index/customers.html', customers = db_search)
    
    # Details Editing Form Handling
    elif request.method == 'POST':

        # Get Dictionary keys and values from POST request and gather them into a list (flash them for testing)
        form_keys = []
        is_edit_form = False 
        is_add_form = False
        for k, v in request.form.items():
            form_keys.append({k: v})
            if k == 'store_id':
                is_edit_form = True
            elif k == 'a_store_id':
                is_add_form = True
        flash(form_keys)
        
        # Customer List Logic and query
        if 'clist' in form_keys[0]:
            customer = form_keys[0]['clist']
            clist = customer.split()
           # c_res = db.execute(text('SELECT customer.store_id, customer.customer_id, customer.first_name, customer.last_name, customer.email, customer.active FROM customer' \
            #                        ' WHERE customer.first_name = "{}" AND customer.last_name = "{}"'.format(clist[0], clist[1] )))

            # Updated SELECT query, this grabs all the needed information about a customer, and serves as a template for the info needed for DB insertion
            c_res = db.execute(text('SELECT customer.store_id, customer.customer_id, customer.first_name, customer.last_name, customer.email, customer.active, '\
                                    'address.address, city.city, address.district, address.postal_code, address.phone FROM ((customer INNER JOIN address ON customer.address_id = address.address_id) INNER JOIN city ON address.city_id = city.city_id)'\
                                    ' WHERE customer.first_name = "{}" AND customer.last_name = "{}"'.format(clist[0], clist[1] )))
            
            return render_template('index/customers.html', c_details = c_res)
        
        # If edit form is submitted, perform UPDATE query in db
        if is_edit_form:
            for tag in form_keys:
                if 'store_id' in tag:
                    c_store_id = tag['store_id']
                elif 'customer_id' in tag:
                    c_id = tag['customer_id']
                elif 'first_name' in tag:
                    first_name = tag['first_name']
                elif 'last_name' in tag:
                    last_name = tag['last_name']
                elif 'email' in tag:
                    email = tag['email']
                elif 'active' in tag:
                    isactive = tag['active']
            
            db.execute(text('UPDATE customer SET store_id = "{}", first_name = "{}", last_name = "{}", email = "{}", active = "{}" '\
                            'WHERE customer.customer_id = "{}"'.format(c_store_id, first_name, last_name, email, isactive, c_id)))
            db.commit()
            
            customer_list = db.execute(text('SELECT customer.customer_id, customer.first_name, customer.last_name FROM customer'))
            
            return render_template('index/customers.html', customers = customer_list)
        
        # If add form is posted, perform INSERT query
        if is_add_form:
            for tag in form_keys:
                if 'a_store_id' in tag:
                    a_c_store_id = tag['a_store_id']
                elif 'a_customer_id' in tag:
                    a_c_id = tag['a_customer_id']
                elif 'a_first_name' in tag:
                    a_first_name = tag['a_first_name']
                elif 'a_last_name' in tag:
                    a_last_name = tag['a_last_name']
                elif 'a_email' in tag:
                    a_email = tag['a_email']
                elif 'a_active' in tag:
                    a_isactive = tag['a_active']
                elif 'a_address' in tag:
                    a_address = tag['a_address']
                elif 'a_city' in tag:
                    a_city = tag['a_city']
                elif 'a_district' in tag:
                    a_district = tag['a_district']
                elif 'a_postal_code' in tag:
                    a_postal_code = tag['a_postal_code']
                elif 'a_phone' in tag:
                    a_phone = tag['a_phone']

            # INSERT statements require a three-step process, since there are foriegn keys connecting customer, address, city, and country tables
            # First INSERT into city table
            db.execute(text('INSERT INTO city (city, country_id) VALUES ("{}", 103)'.format(a_city)))
            db.commit()

            # Second is to use the above city_id key to INSERT into the address table
            db.execute(text('INSERT INTO address (address, city_id, district, postal_code, phone, location)'\
                            ' VALUES ("{}", (SELECT city_id FROM city WHERE city="{}"),'\
                            '"{}", "{}", "{}", POINT (-112.8185647 ,49))'.format(a_address, a_city, a_district, a_postal_code, a_phone)))
            db.commit()

            # Third is to use the above address_id to INSERT into the customer table (we'll default into store 1 for the sake of this application)
            db.execute(text('INSERT INTO customer (store_id, first_name, last_name, email, address_id, active)'\
                            ' VALUES (1, "{}", "{}", "{}",'\
                            ' (SELECT address_id FROM address WHERE address = "{}"), 1)'.format(a_first_name, a_last_name, a_email, a_address)))
            db.commit()
            
            # customer_id is AUTO_INCREMENT FIX BEFORE MOVING ON!!!
            #db.execute(text('INSERT INTO customer (store_id, first_name, last_name, email, active) VALUES '\
            #                '({}, {}, {}, {}, {})'.format(a_c_store_id, a_first_name, a_last_name, a_email, a_isactive)))
            #db.commit()
            customer_list = db.execute(text('SELECT customer.customer_id, customer.first_name, customer.last_name FROM customer'))

            return render_template('index/customers.html', customers = customer_list)
        
    return render_template('index/customers.html', customers = customer_list)
