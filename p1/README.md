
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">CS50w Project 1: Books</h3>

  <p align="center">
    My solution for Project 1 for CS50's Web Programming with Python and JavaScript
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

The goal of the project is to build a book review website. There will be a user system(to login and register). On the page, the user can search for books, leave a review, and see reviews made by other users. Also, there is an integration with the API provided by Goodreads to show extra information about the books.

To solve this, I create a SQL database with 3 tables:
  - users
  - books
  - reviews

There is a file *create_database.sql* with the SQL instructions to replicate the database.

There are 3 important files:
 - import.py: used to fill the database with books stored in the *books.csv* file
 - helpers.py: here I defined some usefull funcionts for the program like:
   * goodreads_lookup: to look up info of book using the Goodreads' API
   * login_required: it's a decorator to only allow the registered users access to the resources.
 - application.py: here is all the code of the app, the set up of the flask app and its views.

In the *templates* are the HTML templates for the dashboard.

### Built With
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [PostgreeSQL](https://www.postgresql.org/)
* [Bootstrap](https://getbootstrap.com)



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

1. Set up an PostgresSQL Database(you can get one for free in [Heroku](https://heroku.com)), for this project you cand use any SQL database, even SQLITE3. And take note of the URI, you will need it.
```sh
$ export DATABASE_URL=<YOUR-URL>
```
2. Set up an developer account on Goodreads and take note of your api key
```sh
$ export GOODREADS_API_KEY=<YOUR-API-KEY>
```
 

### Installation

2. Set up a virtual environment and active it
```sh
$ python3 -m venv venv
$ source ven/bin/activate
```
3. Install requeriments
```sh
$ pip install -r requirements.txt
```
4. Set up Flask
```sh
$ export FLASK_APP=application.py
```



<!-- USAGE EXAMPLES -->
## Usage

Before to start using the app, we are going to fill the database with some some books.
```sh
$ python3 import.y
```
Now we can run the server
```sh
$ flask run
```
Let's open a browers a go to http://localhost:5000 to start usin the app.



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Your Name - [@arielsperduti](https://twitter.com/arielsperduti)