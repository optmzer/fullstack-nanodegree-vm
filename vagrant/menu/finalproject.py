#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# Imports DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

################ Create Flask app ################

app = Flask(__name__)

################ Create Connection to DB ################
# init connection with DB
engine = create_engine('sqlite:///restaurantmenu.db')

# Connection between class def and corresp table in DB
Base.metadata.bind = engine
# Create delete and other commands Alchemy does via an interface called a Session
DBSession = sessionmaker(bind=engine)

session = DBSession()

################ Getters/Setters ################

def getRestaurant(restaurantID):
    return session.query(Restaurant).filter_by(id = restaurantID).one()

def getMenuItems(restaurantID):
    return session.query(MenuItem).filter_by(restaurant_id = restaurantID).all()

def getMenuItem(restaurantID, menuItemID):
    restaurant = getRestaurant(restaurantID)
    menuItem = session.query(MenuItem).filter_by(restaurant_id = restaurant.id, id = menuItemID).one()
    print("L33 MenuItem " + menuItem.name)
    return menuItem

################ Routs ################
################ Restaurant ################

# Show all restaurants
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

# Create new restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant(restaurantID):
    return render_template('newrestaurant.html')

# Edit restaurant
@app.route('/restaurant/<int:restaurantID>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurantID):
    return render_template('editrestaurant.html')

# Delete restaurant 
@app.route('/restaurant/<int:restaurantID>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurantID):
    return render_template('deleterestaurant.html')

################ Routs ################
################ MenuItem ################
# Show restaurant menu items
@app.route('/restaurant/<int:restaurantID>/menu/')
def showMenuItems(restaurantID):
    print("############### Show restaurant menu ###############")
    restaurant = getRestaurant(restaurantID)
    print("Restaurant = %s" % restaurant.name)
    menuItems = getMenuItems(restaurantID)
    return render_template("menu.html", restaurant=restaurant, menuItems=menuItems)

# Create new menu item
@app.route('/restaurant/<int:restaurantID>/menu/new/', methods=['GET', 'POST'])
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

# Edit menu item
@app.route('/restaurant/<int:restaurantID>/menu/<int:menuID>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurantID, menuID):
    restaurant = getRestaurant(restaurantID)
    item = getMenuItem(restaurantID, menuID)
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
# Delete menu item
@app.route('/restaurant/<int:restaurantID>/menu/<int:menuID>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurantID, menuID):
    restaurant = getRestaurant(restaurantID)
    item = getMenuItem(restaurantID, menuID)
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