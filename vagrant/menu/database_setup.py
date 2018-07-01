import sys
from sqlalchemy import Column, ForeignKey, Integer, String 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Because I use Vagrant from Udacity SQLAlchemy is 
# already installed on Virtual Machine(VM)
# Base is a declarative Data Base
Base = declarative_base()

########
class Restaurant(Base):

    __tablename__ = 'restaurant'

    # Mapper
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

########
class MenuItem(Base):

    __tablename__ = 'menu_item'

    # Mapper
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    # restaurant_id is a foreign key
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restauratn_id = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course
        }


########## Insert at the end of the file ##########
engine = create_engine('sqlite:///restaurantmenu.db')

# Adds classes as new tables in our DB
Base.metadata.create_all(engine)
