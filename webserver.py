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
        try:
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
                output += "<a href = 'restaurants/new'>Add New Restaurant</a> <br/>"
                allRestaurants = session.query(Restaurant).all()
                for restaurant in allRestaurants:
                    output += "<br/><br/> %s <br/>" % restaurant.name
                    output += "<a href = 'restaurants/%s/edit'>Edit</a> <br/>" % restaurant.id
                    output += "<a href = 'restaurants/%s/delete'>Delete</a> <br/>" % restaurant.id 
                output += "<br/><br/><a href = '/hola' >Spanish Language</a>"
                output += "</body></html>"
                self.wfile.write(output.encode())
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1> %s </h1>" % myRestaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form></body></html>"
                    self.wfile.write(output.encode())
                    
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1> Are you sure you want to delete: <i><b>%s</b></i> ?</h1>" % myRestaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/delete' >" % restaurantIDPath
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form></body></html>"
                    self.wfile.write(output.encode())
                
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name'>"
                output += "<input type = 'submit' value = 'Create'> "
                output += "<input type = 'submit' value = 'Cancel'>"
                output += "</form></body></html>"
                self.wfile.write(output.encode())
                
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
            
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    if messagecontent[0].decode("utf-8") and (not messagecontent[0].decode("utf-8").isspace()):
                        newRestaurant = Restaurant(name=messagecontent[0].decode("utf-8"))
                        session.add(newRestaurant)
                        session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0].decode("utf-8")
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        session.delete(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
            
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
