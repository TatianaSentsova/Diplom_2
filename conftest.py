import pytest
import allure
from fake_data import FakeData
from api_shop import ApiRequests, ApiBodyBuilder
from collections import namedtuple


@allure.step('Получаем тело запроса с валидными данными для создания пользователя')
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


@allure.step('Создаем пользователя и получаем кортеж с данными пользователя')
@pytest.fixture
def new_user():
    email = FakeData.email()
    password = FakeData.password()
    name = FakeData.name()
    user_body = ApiBodyBuilder.build_user_body(email, password, name)
    ApiRequests.create_user(user_body)
    UserData = namedtuple('UserData', ['email', 'password', 'name'])
    yield UserData(email, password, name)
    login_pass_body = ApiBodyBuilder.build_login_pass_body(email, password)
    response = ApiRequests.login_user(login_pass_body)
    token = response.json()['accessToken']
    ApiRequests.delete_user(token)


@allure.step('Создаем пользователя, получаем кортеж с токеном авторизации и данными пользователя')
@pytest.fixture
def authorized_user():
    email = FakeData.email()
    password = FakeData.password()
    name = FakeData.name()
    user_body = ApiBodyBuilder.build_user_body(email, password, name)
    ApiRequests.create_user(user_body)
    login_pass_body = ApiBodyBuilder.build_login_pass_body(email, password)
    response = ApiRequests.login_user(login_pass_body)
    token = response.json()['accessToken']
    UserData = namedtuple('UserData', ['email', 'password', 'name', 'token'])
    yield UserData(email, password, name, token)
    ApiRequests.delete_user(token)
