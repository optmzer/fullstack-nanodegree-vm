from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

# Connection between class def and corresp table in DB
Base.metadata.bind = engine
# Create delete and other commands Alchemy does via an interface called a Session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Creating new tables
# I had to add id as python compiler come back with an error 
# MenuItem does not have prop restaurant. prop restaurant also had to be changed to restaurant_id
myFirstRestaurant = Restaurant(name = 'Pizza Palace')
# Further same as Git
# Add myFirstRestaurant to the staging area
# Commit session
# session.add(myFirstRestaurant)
# session.query(Restaurant).all #Returns list of entries
# So I need an Iterator to list through them or for loop
cheesepizza = MenuItem(name='Cheese Pizza', description='Made with all natural ingredients and fresh cheddar chees!', course='Entree', price='$9.99', restaurant_id = myFirstRestaurant.id)
# session.add(cheesepizza)


# session.commit()

# This syntax allows to use Row names as object variables
# firstResult = session.query(MenuItem).first()
# print(firstResult.name + " " + firstResult.description)