import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from movieapp.db import get_db

# Create blueprint for the index view
bp = Blueprint('index' ,__name__, url_prefix='/index')

# Create different routes for each of the pages, and define the functionality of each
@bp.route('/home', methods=('GET', 'POST'))
def home():
    return render_template('index/home.html')

@bp.route('/movies', methods=('GET', 'POST'))
def movies():
    return render_template('index/movies.html')

@bp.route('/customers', methods=('GET', 'POST'))
def customers():
    return render_template('index/customers.html')