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
class webserverHandler(BaseHTTPRequestHandler):

    restaurant_to_modify = ""


################ Data Base functions ################
    def getSessionDB(self):
        # init connection with DB
        engine = create_engine('sqlite:///restaurantmenu.db')

        # Connection between class def and corresp table in DB
        Base.metadata.bind = engine
        # Create delete and other commands Alchemy does via an interface called a Session
        DBSession = sessionmaker(bind=engine)
        return DBSession()


    def getListOfRestaurants(self):
        session = self.getSessionDB()
        return session.query(Restaurant).all()

    def addRestaurant(self, name):
        # TODO: Add restaurant to DB
        session = self.getSessionDB()
        restaurant = Restaurant(name = name)
        session.add(restaurant)
        session.commit()

    def deleteRestaurant(self, name):
        # TODO: Add restaurant to DB
        output = "TODO: "
        return output

    def updateRestaurant(self, oldName,  newName):
        # TODO: Add restaurant to DB
        output = "TODO: "
        return output

    ################ HTML FORMS ################
    def form_create(self):
        # Creates new Restaurant in DB
        output = '''
        <div>
            <a href="/restaurants">HOME</a>
            <form method='POST' enctype='multipart/form-data' action='/restaurants'>
                <p>Create new restaurant</p>
                <label for="create">Restaurant name: </label>
                <input type="text" name="message" id="create" required="true" placeholder="Type name...">
                <input type="submit" value="Create">
            </form>
        </div>
        '''
        return output

    def form_edit(self, name):
        output =  '''
        <div>
            <a href="/restaurants">HOME</a>
            <p>Edit restaurant name</p>
            <form method='POST' enctype='multipart/form-data' action='/restaurants'>
                <h3>{}</h3>
                <input name='message' type='text'>
                <input type='submit' value='Submit'>
                <input type='reset' value='Cancel'>
            </form>
        </div>
        '''
        return output.format(name)

    def form_delete(self, name):
        if name == "":
            name = "Empty"
        output =  '''
        <div>
            <a href="/restaurants">HOME</a>
            <form method='POST' enctype='multipart/form-data' action='/restaurants'>
                <p>Please confirm permanent delition of</p>
                <h3>{} restaurant from our database.</h3>
                <p><b>WARNING!!!</b> Delition is permanent.</p>
                <input type='submit' value='Delete'>
            </form>
        </div>
        '''
        return output.format(name)

    def restaurant_div(self, name):
        output = '''
            <div class="restaurant-name">
                <h2>{}</h2>
                <a href='/edit'>EDIT</a>
                <a href='/delete'>DELETE</a>
            </div>
        '''
        return output.format(name)

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
                output += "<a href='/new'>CREATE NEW</a>"
                output += "<ul>"
                for restaurant in restaurants:
                    output += "<li>"
                    output += self.restaurant_div(restaurant.name) 
                    output += "</li>"
                output += "</ul>"
                output += "</body></html>" 

                self.wfile.write(output.encode())
                return

            if self.path.endswith("/edit"):
                # Edit restaurant name
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                output = "<html lang='en'><body>" \
                    "" + self.form_edit(self.restaurant_to_modify) + \
                    "</body></html>"
                self.wfile.write(output.encode())
                return

            if self.path.endswith("/delete"):
                # Confirm deletion page
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                output = "<html lang='en'><body>" \
                    "" + self.form_delete("") + \
                    "</body></html>"
                self.wfile.write(output.encode())
                return

            if self.path.endswith("/new"):
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
            self.send_response(301)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # HEADERS are now in dict/json style container
            ctype, pdict = cgi.parse_header(
                self.headers['content-type'])

            # boundary data needs to be encoded in a binary format
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                
            # TODO: Create logic inhere
            # POST method has to know whether it is add || delete || update
            output = "<html lang='en'><body>" 
            output += "<a href='/restaurants'>HOME</a>" 
            output += "<p>This is POST responce page...</p>" 
            # If str.decode() not used string is written as "b'string'"
            output += "<h2>Restaurant: %s created</h2>" % messagecontent[0].decode()
            output += "</body></html>" 
            self.wfile.write(output.encode())
            # print(output)
            # Original file from Udacity has no return mathod in POST. Why???
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
        port = 8000
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