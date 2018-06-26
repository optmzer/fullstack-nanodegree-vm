#!/usr/bin/env python3
# The BaseHTTPServer module has been merged into http.server in Python 3.
# Every time you see BaseHTTPServer just use http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

# Handler
# class ClassName(ParentClass) == class ClassName extends ParentClass
class webserverHandler(BaseHTTPRequestHandler):

    form_html = '''
        <form method='POST' enctype='multipart/form-data' action='/hello'>
            <h3>What would you like me to say?</h3>
            <input name='message' type='text'>
            <input type='submit' value='Submit'>
        </form>
    '''

    def do_GET(self):
        # GET method provides path variable
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                output = "<html lang='en'><body>" \
                    "<p>This is Hello Page!</p>" \
                    "<a href='/privet'>To Privet page</a>" \
                    "<h1>OK, How about this?</h1>" + self.form_html + \
                    "</body></html>" 

                self.wfile.write(output.encode())
                return
            if self.path.endswith("/privet"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()

                output = "<html lang='en'><body>" \
                    "<p>Russia language uses charset=ISO-8859-1. Need to learn how to setup a server to render this correctly</p>"\
                    "<a href='/hello'>To hello page</a>" \
                    "<h1>OK, How about this?</h1>" + self.form_html + \
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
            
            # output slash "\" does not work inhere because of 
            # % messagecontent[0].decode() and self.form_html
            # compiler does not know what to do with them
            # better to write as output +=.
            output = "<html lang='en'><body>" 
            output += "<p>This is POST responce page...</p>" 
            output += "<a href='/hello'>To hello page</a>" 
            output += "<h1>OK, How about this?</h1>" 
            # If str.decode() not used string is written as "b'string'"
            output += "<h2>message: %s</h2>" % messagecontent[0].decode()
            output += self.form_html
            output += "</body></html>" 
            self.wfile.write(output.encode())
            # print(output)
            # Original file from Udacity has no return mathod in POST. Why???
            return
 
        except :
            print("Exception thrown...")
            raise
    

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