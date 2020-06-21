Music Management Platform
===========

Manage your music easily.


Installation
------------

Install packages.

    $ pip install -r requirements.txt


Running the application
-----------------------

::

    $ flask init-db
    $ flask run

Open http://127.0.0.1:5000 in a browser.


Libraries
------------

### Backend

- [Flask](http://flask.pocoo.org/).
- [python-dotenv](https://pypi.org/project/python-dotenv/) for the environment.

### Frontend

- [Bootstrap](http://getbootstrap.com/) for the global style.


Structure
---------

Everything is contained in the `src/` folder.

- There you have the classic `static/` and `templates/` folders. The `templates/` folder contains layout and `static/` contain `music/` for uploading audio, `css/`, and `js/`.
- The `__init__.py` script contains create_app function for application factory.
- The `db.py` script to create connection to sqlite and for `flask init-db` command to initialize database.
- The `auth.py` script contains route for user related functions such as `login`, `logout` and `register`.
- The `music.py` script contains route for all the music related functions.
- The `schema.sql` contains the sql queries need to initialize database.
