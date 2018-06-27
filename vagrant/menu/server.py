#!/usr/bin/env python3
# The BaseHTTPServer module has been merged into http.server in Python 3.
# Every time you see BaseHTTPServer just use http.server
# imports Server
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

# Imports DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# TODO: Make a connection to DB
# Retrive the data
# loop through restaurant list

# Handler
# class ClassName(ParentClass) == class ClassName extends ParentClass

################ Create Connection to DB ################
# init connection with DB
engine = create_engine('sqlite:///restaurantmenu.db')

# Connection between class def and corresp table in DB
Base.metadata.bind = engine
# Create delete and other commands Alchemy does via an interface called a Session
DBSession = sessionmaker(bind=engine)

session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):

################ Data Base functions ################

    def getListOfRestaurants(self):
        return session.query(Restaurant).all()

    def addRestaurant(self, name):
        # Adds new restaurant to DB
        # Does not do any checks yet
        restaurant = Restaurant(name = name)
        session.add(restaurant)
        session.commit()

    def deleteRestaurant(self, id):
        # Delete a restaurant from DB
        # Does not do any checks
        restaurant = session.query(Restaurant).filter_by(id = id).one()
        session.delete(restaurant)
        session.commit()
        print("L51 %d, Restaurant %s deleted" %(restaurant.id, restaurant.name))

    def updateRestaurant(self, restaurant, newName):
        # Update Restaurant name DB
        # Does not do any checks

        # self.getRestaurant(id)
        print("Old name = %s " % restaurant.name)
        restaurant.name = newName
        print("New name = %s " % restaurant.name)
        session.add(restaurant)
        session.commit()

    def getRestaurant(self, id):
        restaurant = session.query(Restaurant).filter_by(id=id).first()
        print("L67 getRestaurant() id = %d, restaurant.id = %d, restaurant.name = %s" % (id, restaurant.id, restaurant.name))
        return restaurant

    ################ HTML FORMS ################
    def form_create(self):
        # Creates new Restaurant in DB
        output = '''
        <div>
            <a href="/restaurants">HOME</a>
            <form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                <p>Create new restaurant</p>
                <label for="create">Restaurant name: </label>
                <input type="text" name="newRestaurantName" id="create" required="true" placeholder="Type name...">
                <input type="submit" value="Create">
            </form>
        </div>
        '''
        return output

    def form_edit(self, name, id):
        output =  '''
        <div>
            <a href="/restaurants">HOME</a>
            <p>Edit restaurant name</p>
            <form method='POST' enctype='multipart/form-data' action='/restaurants/{id}/edit'>
                <h3>{name}</h3>
                <input name='editRestaurantName' type='text' required='true'>
                <input type='submit' value='Submit'>
                <input type='reset' value='Cancel'>
            </form>
        </div>
        '''
        return output.format(id=id, name=name)

    def form_delete(self, id, name):
        output =  '''
        <div>
            <a href="/restaurants">HOME</a>
            <form method='POST' enctype='multipart/form-data' action='/restaurants/{id}/delete'>
                <p>Please confirm permanent delition of</p>
                <h3>{name} restaurant from our database.</h3>
                <p><b>WARNING!!!</b> Delition is permanent.</p>
                <input type='submit' value='Delete'>
            </form>
        </div>
        '''
        return output.format(id=id, name=name)

    def restaurant_div(self, name, id):
        output = '''
            <div class="restaurant-name">
                <h2>{name}</h2>
                <a href='/restaurants/{id}/edit'>EDIT</a>
                <a href='/restaurants/{id}/delete'>DELETE</a>
            </div>
        '''
        return output.format(name=name, id=id)

    ################ SERVER RESPONCES ################

    def do_GET(self):
        # GET method provides path variable
        # List all restaurants in DB
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                restaurants = self.getListOfRestaurants()

                output = "<html lang='en'><body>"
                output += "<a href='/restaurants/new'>CREATE NEW</a>"
                output += "<ul>"
                for restaurant in restaurants:
                    output += "<li>"
                    output += self.restaurant_div(restaurant.name, restaurant.id) 
                    output += "</li>"
                output += "</ul>"
                output += "</body></html>" 

                self.wfile.write(output.encode())
                return

            if self.path.endswith("/edit"):
                restaurantIdPath = self.path.split('/')[2]

                restaurant = self.getRestaurant(int(restaurantIdPath))

                # Edit restaurant name
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                output = "<html lang='en'><body>" \
                    "" + self.form_edit(restaurant.name, restaurant.id) + \
                    "</body></html>"
                self.wfile.write(output.encode())
                return

            if self.path.endswith("/delete"):

                restaurantIdPath = self.path.split('/')[2]
                restaurant = self.getRestaurant(int(restaurantIdPath))

                # Confirm deletion page
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                output = "<html lang='en'><body>" \
                    "" + self.form_delete(restaurant.id, restaurant.name) + \
                    "</body></html>"
                self.wfile.write(output.encode())
                return

            if self.path.endswith("/restaurants/new"):
                # Edit restaurant name
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                output = "<html lang='en'><body>" \
                    "" + self.form_create() + \
                    "</body></html>"
                self.wfile.write(output.encode())
                return

        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    def do_POST(self):
        try:
            # HEADERS are now in dict/json style container
            ctype, pdict = cgi.parse_header(
                self.headers['content-type'])

            # boundary data needs to be encoded in a binary format
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")


            if self.path.endswith("/restaurants/new"):

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                # Add new restaurant to DB
                self.addRestaurant(messagecontent[0].decode())

                # Send responce to the client
                self.send_response(301)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                # Location - redirects page to whatever you set to.
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            if self.path.endswith("/delete"):
                restaurantIdPath = self.path.split('/')[2]

                id = int(restaurantIdPath)

                # Add new restaurant to DB
                self.deleteRestaurant(id)

                # Send responce to the client
                self.send_response(301)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                # Location - redirects page to whatever you set to.
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            if self.path.endswith("/edit"):
                restaurantIdPath = self.path.split('/')[2]

                restaurant = self.getRestaurant(int(restaurantIdPath))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newName = fields.get('editRestaurantName')

                # Add new restaurant to DB
                self.updateRestaurant(restaurant, newName[0].decode())

                # Send responce to the client
                self.send_response(301)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
 
        except :
            print("Exception thrown...")
            raise
    

############# end class 

# Main
# It is added at the end of the file so python interpreter
# can immediatly run it as it translates the script
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print ("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
    # Build in interupt inot python exits when user
    # holds ctrl+C. So no additional code needed
        print("^C entered, stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()