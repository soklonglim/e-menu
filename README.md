# Full Stack Foundations Course (Udacity)
Fundamental of back-end web development by creating our own web application from the ground up using iterative development


## Lesson 1
- CRUD: Create, Read, Update, Delete
- ORM (Object Relational Mapping) allows applicate communicate with sqlite database (for this course we use SQLAlchemy: opensource ORM for python)
- We will use Vagrant VM with SQLAlchemy installed to this course
- 'database_setup.py' creates database
- 'crud_operations.py' contains some operations to see if database is working properly
- 'lotsofmenus.py' adds menus item into database

## Lesson 2
- build http server that runs until (ctrl c) is pressed 
- server will be able to response to the client via http GET, POST, DELETE
- get server and database to commuicate by using http GET to list all the restaurants in the database to the webpage
- add 3 now buttons to the page: add new restaurant, edit, and delete restaurant

## Lesson 3
- Web Application Framework or simply Web Framework represents a collection of libraries and modules that enables a web application developer to write applications without having to bother about low-level details such as protocols, thread management etc. (tutorailspoint.com)
- Flask framework, a web application framework written in python. (tutorialspoint.com) 
- Create standard url routing (lession 3 part 7). 
- NOTE: make sure database has what you think it has. Any practice example that modifies the database will later mess up the content of the database, and it will be trouble for next step. (just recreate new database with new data stored after each example)
- Create routing then generate templates for rendering
- Render HTML templates from a templates dir rather than reconstructing html each time we need show data on web page
- create url for different page with different purpose (add, delete, update) page (easy to make change to url path (one stop change))
- add: create new item to be added. If POST request, add the item to database and render back to menu page. Otherwise, reqest for add new item page.
- edit: find the item to be edited. If POST request, edit the item, update database and render back to menu page. Otherwise, request for edite template.
- delete: find the item to be deleted. If POST request, delete the item, update database and render back to menu page. Otherwise, request for delete template.
- create a RESTful API for other application to retrieve data from webpage (restaurant, menue) for advertising like purpose. They just need data. There is no need of HTML or CSS. API should return JSON (JavaScript Object Notation) file to the request.
- add serialize function to database_setup.py to serialize data into json format

