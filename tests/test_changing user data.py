import pytest
import allure
from api_shop import ApiRequests, ApiBodyBuilder
from data import ResponseMessage
from fake_data import FakeData


class TestChangingUserData:
    @allure.title("Успешное изменение данных авторизованного пользователя")
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_changing_user_data_with_sign_in(self, authorized_user, field):
        body = ApiBodyBuilder.build_user_body(authorized_user.email, authorized_user.password, authorized_user.name)
        error_data = f'{body[field]}f'
        body[field] = error_data
        response = ApiRequests.changing_data_user(authorized_user.token, body)
        assert response.status_code == 200
        assert response.json()['success']

    @allure.title("Невозможно измененить данные пользователя без авторизации")
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_changing_user_data_without_sign_in(self, authorized_user, field):
        body = ApiBodyBuilder.build_user_body(authorized_user.email, authorized_user.password, authorized_user.name)
        error_data = f'{body[field]}f'
        body[field] = error_data
        token = ''
        response = ApiRequests.changing_data_user(token, body)
        print(response.json())
        assert response.status_code == 401
        assert response.json() == ResponseMessage.YOU_SHOULD_BE_AUTHORISED
