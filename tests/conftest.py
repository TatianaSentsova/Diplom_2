import pytest
from fake_data import FakeData
from api_shop import ApiRequests, ApiBodyBuilder


@pytest.fixture
def request_user_body():
    email = FakeData.email()
    password = FakeData.password()
    name = FakeData.name()
    user_body = ApiBodyBuilder.build_user_body(email, password, name)
    login_pass_body = ApiBodyBuilder.build_login_pass_body(email, password)
    yield user_body
    response = ApiRequests.login_user(login_pass_body)
    token = response.json()['accessToken']
    ApiRequests.delete_user(token)

@pytest.fixture
def user_login_pass():
    email = FakeData.email()
    password = FakeData.password()
    name = FakeData.name()
    user_body = ApiBodyBuilder.build_user_body(email, password, name)
    login_pass_body = ApiBodyBuilder.build_login_pass_body(email, password)
    ApiRequests.create_user(user_body)
    yield login_pass_body.copy()
    response = ApiRequests.login_user(login_pass_body)
    token = response.json()['accessToken']
    ApiRequests.delete_user(token)
