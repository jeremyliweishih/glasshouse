# all the imports
import os
import sqlite3
from geopy.geocoders import Nominatim
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_heroku import Heroku
#from flask.ext.cache import Cache

# engine = create_engine('postgresql://localhost/g', echo=True)

# Session = sessionmaker()
# db.session = Session()


app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # load config from this file , glassHouse.py

# Load default config and override config from an environment variable
app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, 'glassHouse.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

# app.config.from_envvar('GLASSHOUSE_SETTINGS', silent=True)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgrqesql://localhost/g'
# db = SQLAlchemy(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gdjtdztginlgus:37e7e34fd7b6a94edb94de63d9bb1ec5a65157e70eab9f6df41046ddf52bb3a1@ec2-54-225-242-74.compute-1.amazonaws.com:5432/dfddds05ds0luj'
app.config["CACHE_TYPE"]="simple"

#app.cache = Cache(app)
heroku = Heroku(app)
db = SQLAlchemy(app)

class House(db.Model):
    __tablename__ = 'houses'
    id = db.Column('house_id', db.Integer, primary_key=True)
    address = db.Column(db.String(60))
    x_coord = db.Column(db.Float)
    y_coord = db.Column(db.Float)
    rent = db.Column(db.Integer)

    def __init__(self, address, x_coord, y_coord, rent):
        self.address = address
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.rent = rent

class User(db.Model):
    __tablename__ ='users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    student_id = db.Column(db.Integer)
    username = db.Column(db.String(10))
    password = db.Column(db.String(10))

    def __init__(self, email, student_id, username, password):
        self.email = email
        self.student_id = student_id
        self.username = username
        self.password = password



db.create_all()


@app.route('/')
def show_entries():

    entries = []
    for instance in db.session.query(House).order_by(House.id):
        entries.append(instance)

    print(entries)

    return render_template('main.html', entries=entries)

@app.route('/id/<id>')
def get_by_id(id):
   
    sanitized_id = int(id)
    
    for instance in db.session.query(House).filter_by(id=str(sanitized_id)):
        entry = instance
    
    output = json.dumps({'address': entry.address, 'rent': entry.rent})
    return output

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    
    geolocator = Nominatim()
    location = geolocator.geocode(request.form['address'])
    print(request.form['address'])
    print((location.latitude, location.longitude))

    ed_house = House(address = request.form['address'], x_coord = location.longitude, y_coord = location.latitude, rent = request.form['rent'])
    db.session.add(ed_house)
    db.session.commit()
   

    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/add_user', methods=['POST'])
def add_user():
    new_user = User(email = request.form['email'], student_id = request.form['studentid'], username = request.form['username'], password = request.form['password'])
    db.session.add(new_user)
    db.session.commit()

    flash('Thanks For Signing Up')
    flash(request.form['username'])
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))

    entries = []
    for instance in db.session.query(House).order_by(House.id):
        entries.append(instance)

    return render_template('main.html', error=error, entries=entries)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))



############## RESTful API REQUESTS #############

@app.route('/houses', methods=['GET'])
def get_houses():
    entries = []
    for instance in db.session.query(House).order_by(House.id):
        entries.append({'id': instance.id,
                                   'address': instance.address,
                                   'rent': instance.rent,
                                   'longitude': instance.x_coord,
                                   'latitude': instance.y_coord})

    return json.dumps(entries)
@app.route('/houses/<rent>', methods=['GET'])
def get_houses_by_rent(rent):
    sanitized_rent = int(rent)
    entries = []
    for instance in db.session.query(House).filter_by(rent=str(sanitized_rent)):
        entries.append({'id': instance.id,
                                   'address': instance.address,
                                   'rent': instance.rent,
                                   'longitude': instance.x_coord,
                                   'latitude': instance.y_coord})

    return json.dumps(entries)


@app.route('/house/<id>', methods=['GET'])
def get_a_house(id):
    # db = get_db()
    sanitized_id = int(id)
    entry = ""
    # cur = db.execute('select * from entries where id='+str(sanitized_id))
    for instance in db.session.query(House).filter_by(id=str(sanitized_id)):
        entry = instance
    # entry = cur.fetchone()
    output = json.dumps({'id': instance.id,
                                   'address': instance.address,
                                   'rent': instance.rent,
                                   'longitude': instance.x_coord,
                                   'latitude': instance.y_coord})
    return output

@app.route('/house', methods=['POST'])
def create_house():
    address = request.args.get('address', None)
    rent = request.args.get('rent', None)
    
    geolocate = Nominatim()
    loc = geolocate.geocode(address)
    ###need to account for invalid address
    house = House(address = address, x_coord = loc.longitude, y_coord = loc.latitude, rent = rent)
    db.session.add(house)
    db.session.commit()

    return('',201)





@app.route('/users', methods=['GET'])
def get_all_users():
    entries = []
    for instance in db.session.query(User).order_by(User.id):
        entries.append({'id': instance.id,
                                   'email': instance.email})

    return json.dumps(entries)

@app.route('/user/<student_id>', methods=['GET'])
def get_a_user(student_id):
    sanitized_id = int(student_id)

    entry = ""

    for instance in db.session.query(User).filter_by(student_id=str(sanitized_id)):
        entry = instance

    output = json.dumps({'id': instance.id,
                                   'email': instance.email,
                                   'student_id': instance.student_id})
    return output

@app.route('/user', methods=['POST'])
def make_user():
    email = request.args.get('email', None)
    student_id = request.args.get('student_id', None)
    username = request.args.get('username', None)
    password = request.args.get('password', None)


    new_user = User(email = email, student_id = student_id, username = username, password = password)
    db.session.add(new_user)
    db.session.commit()

    return('',201)


# def connect_db():
#     """Connects to the specific database."""
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv

# def init_db():
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()

# @app.cli.command('initdb')
# def initdb_command():
#     """Initializes the database."""
#     init_db()
#     print('Initialized the database.')

# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db

# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()
