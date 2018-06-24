#!/usr/bin/env python3
# The BaseHTTPServer module has been merged into http.server in Python 3.
# Every time you see BaseHTTPServer just use http.server
from http.server import BaseHTTPRequestHandler, HTTPServer

# Handler
# class ClassName(ParentClass) == class ClassName extends ParentClass
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # GET method provides path variable
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html lang='en'><body>"
                output += "<p>This is Hello Page!</p>"
                output += "<a href='/privet'>To Privet page</a>"
                output += "</body></html>"

                self.wfile.write(output.encode())
                return
            if self.path.endswith("/privet"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=ISO-8859-1')
                self.end_headers()

                output = "<html lang='en'><body>"
                output += "<p>Russia language uses charset=ISO-8859-1. Need to learn how to setup a server to render this correctly</p>"
                output += "<a href='/hello'>To hello page</a>"
                output += "</body></html>"
                self.wfile.write(output.encode())
                return

        except IOError:
            self.send_error(404, "File not found %s" % self.path)


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