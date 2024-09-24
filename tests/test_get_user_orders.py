import allure
from api_shop import ApiRequests, ApiBodyBuilder
from data import Ingredients, ResponseMessage


@allure.suite('Получение заказов пользователя')
class TestGetUserOrders:
    @allure.title('Получение списка заказов для авторизованного пользователя')
    @allure.description('''Направляем запрос на создание и авторизацию пользователя. Получив токен авторизации,
                        направляем запрос на создание заказа. После чего, с тем же токеном авторизации, направляем 
                        запрос на получение заказов пользователя. В ответе проверяем код и тело ответа.
                        Созданного пользователя удаляем из базы после теста.''')
    def test_get_user_orders_with_sign_in(self, authorized_user):
        order_body = ApiBodyBuilder.order_body([Ingredients.INGREDIENT])
        ApiRequests.create_order(authorized_user.token, order_body)
        response = ApiRequests.get_user_orders(authorized_user.token)
        assert response.status_code == 200
        assert response.json()['success'] and len(response.json()['orders']) == 1

    @allure.title('Невозможно получить список заказов для неавторизованного пользователя')
    @allure.description('''Направляем запрос на создание и авторизацию пользователя. Получив токен авторизации,
                        направляем запрос на создание заказа. После чего, без токена авторизации, направляем 
                        запрос на получение заказов пользователя. В ответе проверяем код и тело ответа.
                        Созданного пользователя удаляем из базы после теста.''')
    def test_get_user_orders_without_sign_in(self, authorized_user):
        order_body = ApiBodyBuilder.order_body([Ingredients.INGREDIENT])
        ApiRequests.create_order(authorized_user.token, order_body)
        without_token = ''
        response = ApiRequests.get_user_orders(without_token)
        assert response.status_code == 401
        assert response.json() == ResponseMessage.YOU_SHOULD_BE_AUTHORISED
