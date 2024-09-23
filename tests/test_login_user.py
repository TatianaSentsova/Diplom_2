import allure
import pytest
from api_shop import ApiRequests
from data import ResponseMessage


class TestLoginCourier:
    @allure.title("Успешная авторизация зарегистрированного пользователя при заполнении всех обязательных полей")
    def test_login_user(self, user_login_pass):
        response = ApiRequests.login_user(user_login_pass)
        assert response.status_code == 200
        assert response.json()['success']

    @allure.title("Нельзя авторизоваться зарегистрированному пользователю c неправильно заполненным обязательным полем")
    @pytest.mark.parametrize('field', ['email', 'password'])
    def test_login_user_with_error_in_field(self, field, user_login_pass):
        error_data = f'{user_login_pass[field]}f'
        user_login_pass[field] = error_data
        response = ApiRequests.login_user(user_login_pass)
        assert response.status_code == 401
        assert response.json() == ResponseMessage.EMAIL_OR_PASSWORD_ARE_INCORRECT
