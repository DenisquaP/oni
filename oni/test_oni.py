import pytest


def test_basic_route(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"


def test_route_overlap_throws_exception(api):
    @api.route("/home")
    def home(req, resp):
        resp.text = "YOLO"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(req, resp):
            resp.text = "YOLO"


def test_bumbo_test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @api.route("/hey")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get("http://testserver/hey").text == RESPONSE_TEXT


def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/matthew").text == "hey matthew"
    assert client.get("http://testserver/ashley").text == "hey ashley"


def test_default_404_response(client):
    response = client.get("http://testserver/doesnotexist")

    assert response.status_code == 404
    assert response.text == "Not found"


def test_get_post_request(api, client):
    @api.route('/he')
    class Hek:
        def get(self, req, resp):
            resp.text = 'Hi there'

        def post(self, req, resp):
            resp.text = 'POST hi'

    assert client.get("http://testserver/he").text == 'Hi there'
    assert client.post("http://testserver/he").text == 'POST hi'


def test_method_not_allowed(api, client):
    @api.route('/me')
    class Meo:
        def get(self, req, resp):
            resp.text = 'Hi there'

    with pytest.raises(AttributeError):
        client.post("http://testserver/me")
