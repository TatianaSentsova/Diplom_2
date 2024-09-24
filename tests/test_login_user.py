import allure
import pytest
from api_shop import ApiRequests, ApiBodyBuilder
from data import ResponseMessage


class TestLoginCourier:
    @allure.title("Успешная авторизация зарегистрированного пользователя при заполнении всех обязательных полей")
    def test_login_user(self, new_user):
        body = ApiBodyBuilder.build_login_pass_body(new_user.email, new_user.password)
        response = ApiRequests.login_user(body)
        assert response.status_code == 200
        assert response.json()['success']

    @allure.title("Нельзя авторизоваться зарегистрированному пользователю c неправильно заполненным обязательным полем")
    @pytest.mark.parametrize('field', ['email', 'password'])
    def test_login_user_with_error_in_field(self, field, new_user):
        body = ApiBodyBuilder.build_login_pass_body(new_user.email, new_user.password)
        error_data = f'{body[field]}f'
        body[field] = error_data
        response = ApiRequests.login_user(body)
        assert response.status_code == 401
        assert response.json() == ResponseMessage.EMAIL_OR_PASSWORD_ARE_INCORRECT
