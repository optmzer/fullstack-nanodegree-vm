#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash

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

def getRestaurant(restaurantID):
    return session.query(Restaurant).filter_by(id = restaurantID).one()

def getMenuItems(restaurantID):
    print("not supported yet")

def getMenuItem(restaurantID, menuItemID):
    restaurant = getRestaurant(restaurantID)
    menuItem = session.query(MenuItem).filter_by(restaurant_id = restaurant.id, id = menuItemID).one()
    print("L33 MenuItem " + menuItem.name)
    return menuItem

# @app -is a decorator.
# Can be stacked on top of each other. As '/' will call next '/hello' 
# will call next helloWorld().
@app.route('/')
@app.route('/restaurants/<int:restaurantID>/menu/')

def restaurantMenu(restaurantID):
    restaurant = getRestaurant(restaurantID)
    print("Restaurant = %s" % restaurant.name)
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
    return render_template("menu.html", restaurant=restaurant, menuItems=menuItems)


# Task 1: Create route for newMenuItem function here
# Answers to GET and POST requests so I can use forms
@app.route('/restaurants/<int:restaurantID>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurantID):
    restaurant = getRestaurant(restaurantID)

    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'],  description=request.form['description'], price=request.form['price'], restaurant_id = restaurantID)
        session.add(newItem)
        session.commit()
        flash("New menu item created.")
        return redirect(url_for('restaurantMenu', restaurantID = restaurantID))
    else:
        return render_template("newmenuitem.html", restaurant=restaurant)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurantID>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurantID, menu_id):
    restaurant = getRestaurant(restaurantID)
    item = getMenuItem(restaurantID, menu_id)
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['price']:
            item.price = request.form['price']

        session.add(item)
        session.commit()
        flash("Item was updated")
        return redirect(url_for('restaurantMenu', restaurantID = restaurantID))
    else:
        return render_template("editmenuitem.html", restaurant = restaurant, item = item)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurantID>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurantID, menu_id):
    restaurant = getRestaurant(restaurantID)
    item = getMenuItem(restaurantID, menu_id)
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item was deleted.")
        return redirect(url_for('restaurantMenu', restaurantID = restaurantID))
    else:
        return render_template("deletemenuitem.html", restaurant = restaurant, item = item)

if __name__ == '__main__':
    # app.debug = True - Means the server will reloda itself
    # each time it sees chane in code.
    app.secret_key = 'appSecretKey'
    app.debug = True
    # param specifies on port 5000
    app.run(host = '0.0.0.0', port = 5000) 