import pytest
import shelve

from app import create_app

@pytest.fixture()
def app():
    app = create_app(testing=True, db_name = 'test_my_db.db')

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
