from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>'''
            output += '''<h2>What would you like me to say?</h2>'''
            output += '''<input name="message" type="text" >'''
            output += '''<input type="submit" value="Submit"> </form>'''
            output += "<a href = '/hola' >Spanish Language</a>"
            output += "</body></html>"
            self.wfile.write(output.encode())
            print(output)
            return
        
        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body> &#161 Hola ! <a href = '/hello' >English Language</a></body></html>"
            self.wfile.write(message.encode())
            print(message)
            return

        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            allRestaurants = session.query(Restaurant).all()
            for restaurant in allRestaurants:
                output += "<br/><br/> %s <br/>" % restaurant.name
                output += "<a href = '/id/edit'>Edit</a> <br/>"
                output += "<a href = '/delete'>Delete</a> <br/>"
            output += "<br/><br/><a href = '/hola' >Spanish Language</a>"
            output += "</body></html>"
            self.wfile.write(output.encode())
            
        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "Add New Restaurant Page is under construction!"
            output += "</body></html>"
            self.wfile.write(output.encode())
            
        if self.path.endswith("/restaurants/id/edit"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            output = ""
            output += "<html><body>"
            output += "Edite Restaurant Infomation Page is under construction!"
            output += "</body></html>"
            self.wfile.write(output.encode())
            
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)
            
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            ctype, pdict = cgi.parse_header(
                self.headers['content-type'])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "<a href = '/hola' >Spanish Language</a>"
            output += "</body></html>"
            self.wfile.write(output.encode())
            print(output)
            
        except:
            pass

def main():
    try:
        port = 8081
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()
