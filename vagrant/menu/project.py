#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for

# Imports DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

################ Create Connection to DB ################
# init connection with DB
engine = create_engine('sqlite:///restaurantmenu.db')

# Connection between class def and corresp table in DB
Base.metadata.bind = engine
# Create delete and other commands Alchemy does via an interface called a Session
DBSession = sessionmaker(bind=engine)

session = DBSession()

################ Create Flask app ################

app = Flask(__name__)

# @app -is a decorator.
# Can be stacked on top of each other. As '/' will call next '/hello' 
# will call next helloWorld().
@app.route('/')
@app.route('/restaurants/<int:restaurantID>/menu/')

def restaurantMenu(restaurantID):
    restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
    print("Restaurant = %s" % restaurant.name)
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
    return render_template("menu.html", restaurant=restaurant, menuItems=menuItems)


# Task 1: Create route for newMenuItem function here
# Answers to GET and POST requests so I can use forms
@app.route('/restaurants/<int:restaurantID>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurantID):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurantID>/<int:menu_id>/edit/')
def editMenuItem(restaurantID, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurantID>/<int:menu_id>/delete/')
def deleteMenuItem(restaurantID, menu_id):
    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    # app.debug = True - Means the server will reloda itself
    # each time it sees chane in code.
    app.debug = True
    # param specifies on port 5000
    app.run(host = '0.0.0.0', port = 5000) 