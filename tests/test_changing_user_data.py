import pytest
import allure
from api_shop import ApiRequests, ApiBodyBuilder
from data import ResponseMessage


@allure.suite('Изменение данных пользователя')
class TestChangingUserData:
    @allure.title('Успешное изменение данных авторизованного пользователя')
    @allure.description('''Направляем запрос на создание и авторизацию пользователя. Получив токен авторизации,
                        с помощию параметризации проверяем возможность изменения данных пользователя в полях:
                        'email', 'password', 'name'. В ответе проверяем код и тело ответа.
                         Созданного пользователя удаляем из базы после теста.''')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_changing_user_data_with_sign_in(self, authorized_user, field):
        body = ApiBodyBuilder.build_user_body(authorized_user.email, authorized_user.password, authorized_user.name)
        error_data = f'{body[field]}f'
        body[field] = error_data
        response = ApiRequests.changing_data_user(authorized_user.token, body)
        assert response.status_code == 200
        assert response.json()['success']

    @allure.title('Невозможно изменить данные пользователя без авторизации')
    @allure.description('''Создаем пользователя. С помощию параметризации проверяем возможность изменения данных 
                        пользователя в полях: 'email', 'password', 'name' без передачи токена авторизации. 
                        В ответе проверяем код и тело ответа. Созданного пользователя удаляем из базы после теста. ''')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_changing_user_data_without_sign_in(self, authorized_user, field):
        body = ApiBodyBuilder.build_user_body(authorized_user.email, authorized_user.password, authorized_user.name)
        error_data = f'{body[field]}f'
        body[field] = error_data
        without_token = ''
        response = ApiRequests.changing_data_user(without_token, body)
        assert response.status_code == 401
        assert response.json() == ResponseMessage.YOU_SHOULD_BE_AUTHORISED
