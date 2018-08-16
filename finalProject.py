from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

######################### for development stage ####################### 
###Fake Restaurants
##restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
##
##restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
##
###Fake Menu Items
##items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
##item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
########################################################################

# list all the restaurants
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    '''This page will show all my restaurants'''
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

# add new restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    '''This page will be for making a new restaurant'''
    if request.method == 'POST': # when hit 'create'
        newRestaurant = Restaurant(name=request.form['name']) # capture restaurant name
        session.add(newRestaurant) # add new restaurant to database
        session.commit()
        return redirect(url_for('showRestaurants.html')) # redirect to list of all restaurants
    else: 
        return render_template('newRestaurant.html') # bring a create new restaurant page

# edite restaurant
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    '''This page will be for editing restaurant %s " % restaurant_id'''
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']: # if make change
            editedRestaurant.name = request.form['name'] # save changed name
            return redirect(url_for('showRestaurants.html'))
    else:
        return render_template('editRestaurant.html', restaurant=editedRestaurant)

# delete restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    '''This page will be for deleting restaurant %s " % restaurant_id'''
    toBeDeletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(toBeDeletedRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants.html'))
    else:
        return render_template('deleteRestaurant.html', restaurant=toBedeletedRestaurant)

# show menu of a restaurant
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    '''This page is the menu for restaurant %s " % restaurant_id'''
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one() # get restaurant
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all() # get menu list of the restaurant
    return render_template('menu.html', restaurant=restaurant, items=items)

# add new menu item to a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
    '''This page is for making a new menu item for restaurant %s " % restaurant_id'''
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)

# edit menu item of a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    '''This page is for editing menu item %s " % menu_id'''
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

# delete menu item of a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    '''This page is for deleting menu item %s " % menu_id'''
    toBeDeletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(toBeDeletedItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item=toBeDeletedItem, restaurant_id=restaurant_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
