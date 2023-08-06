# Skidward-Web UI

- `Flask-admin` + `Flask-security`

Integrating Flask-admin and Flask-security together, this Web Interface provides custom security for admin user and other users.

Flask-admin provides great template functionality for login, logout, register and related pages. By default, there is no security/ authentication for admin page, anyone can access that.
So in order to restrict the access of admin page so that only administrators could manage all sorts of database tables, not just users and roles, we need to employ flask-security here.

We have done this by overriding the default `ModelView` for admin.


- DATABASE:

Every database has a unique connection string looks similar to one used in `__init__.py` as under:

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:123@localhost/skidwardDB'

Connect your app with the database using such string, replacing <_admin> with an existing <_username> and <123> with <_password> of the username

We have employed Postgresql database with Flask-SQLAlchemy abstraction layer

   - Install Postgres

    $ `brew install postgres`

   - create database

    $ `createdb <dbname>;`

   - create new user (called as 'role' in postgres)

    $ `createuser <user_name>;`

   - Run postgres

    $ `psql`

    #(this logs you in as superuser named "postgres" or your "hostname")

   - list all databases

    postgres=# `\l`

   - list all users

    postgres=# `\du`

   - list all tables

    postgres=# `\dt`


 Tables will be created by `models.py`


- RUN APPLICATION

        $ export FLASK_APP=skidward.web
        $ export DEBUG=true
        $ flask run

        (By default, application will be running on localhost:5000)


- CREATE NEW USER

    (1) CREATE INITIAL ADMIN-USER

    - By default the User Registration allows to create users with 'end-user' role
    - A user with 'end-user' role is not able to create or manage any roles

    - So for the first time creating an admin user, utilize `flask-cli` and run the following command:-

          $ flask user create <email> <password>

    - and then run application by:

          $ flask run

    This will create first user with role 'admin', where we can create any number of users and roles and manage them.

    (2) ADDING MORE USERS

    - After creation of admin user, you can login as admin
    - Register new users with /register URL, or
    - Create and manage users and roles with `flask-admin` built-in CRUD functionality


