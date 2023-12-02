# My own web framework and orm written by python

Technologies used:

* Python
* Webob
* Jinja 2
* Psycopg2
* Gunicorn
* Parse

___

## How to use

1. You need to install all libruaries `pip install -r requirements.txt`
2. Create views in app.py and templates in templates directory
3. Create tables in tables.py
4. Run app using `gunicorn app:app --reload`
