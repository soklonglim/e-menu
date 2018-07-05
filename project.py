from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

from flask import Flask
app = Flask(__name__)


@app.route('/restaurants/<int:restaurant_id>/')
def myRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = ""
    for item in items:
        output += item.name + "<br/>"
        output += item.price + "<br/>"
        output += item.description
        output += "<br/><br/>"
    return output

@app.route('/long')
def HeyLong():
    return "This is Long!!!"

if __name__ == '__main__':
    app.debug = True #server auto reload
    app.run(host='0.0.0.0', port=5001)
