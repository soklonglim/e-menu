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