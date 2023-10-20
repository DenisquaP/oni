from api import API
from orm import ORM
from tables import create

app = API()


DB_SETTINGS = {
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

orm = ORM(DB_SETTINGS)
create(orm)


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"


@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template("index.html", context={
        "name": "oni",
        "title": "Best Framework"
        }).encode()


@app.route('/friends')
def template_friends(req, resp):
    friends = orm.select([], 'test_table')
    print(friends)
    resp.body = app.template("friends.html", context={
        "friends": friends,
        "title": "Friends"
        }).encode()
