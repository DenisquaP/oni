# My own web framework and orm written in python

Technologies used:

* Python
* Webob
* Jinja 2
* Psycopg2
* Gunicorn
* Parse

___

## How to use

1. You need to install all libruaries
1.1 `pip install -r requirements.txt`
2. Create views in app.py and templates in templates directory
3. Create tables in tables.py
4. Run app using `gunicorn app:app --reload`
