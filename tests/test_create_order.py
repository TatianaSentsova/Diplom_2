import pytest
import allure
from api_shop import ApiRequests, ApiBodyBuilder
from data import Ingredients, ResponseMessage


class TestCreateOrder:
    @allure.title("Cоздания заказа c ингредиентами для авторизованного пользователя")
    @pytest.mark.parametrize('ingredients', [[Ingredients.BUN],
                                             [Ingredients.BUN, Ingredients.INGREDIENT],
                                             [Ingredients.BUN, Ingredients.INGREDIENT, Ingredients.INGREDIENT]])
    def test_create_order(self, authorized_user, ingredients):
        order_body = ApiBodyBuilder.order_body(ingredients)
        response = ApiRequests.create_order(authorized_user.token, order_body)
        assert response.status_code == 200
        assert response.json()['success']

    @allure.title("Cоздания заказа c ингредиентами для неавторизованного пользователя")
    @pytest.mark.parametrize('ingredients', [[Ingredients.BUN],
                                             [Ingredients.BUN, Ingredients.INGREDIENT],
                                             [Ingredients.BUN, Ingredients.INGREDIENT, Ingredients.INGREDIENT]])
    def test_create_order_without_sign_in(self, authorized_user, ingredients):
        order_body = ApiBodyBuilder.order_body(ingredients)
        token = ''
        response = ApiRequests.create_order(token, order_body)
        assert response.status_code == 200
        assert response.json()['success']

    @allure.title("Создание заказа без ингрeдиентов")
    def test_create_order_without_ingredients(self, authorized_user):
        order_body = ApiBodyBuilder.order_body([])
        response = ApiRequests.create_order(authorized_user.token, order_body)
        assert response.status_code == 400
        assert response.json() == ResponseMessage.INGREDIENTS_MUST_BE_PROVIDED

    @allure.title("Создание заказа с неправильным id ингрeдиента")
    def test_create_order_error_id_ingredient(self, authorized_user):
        order_body = ApiBodyBuilder.order_body([f'{Ingredients.INGREDIENT}f'])
        response = ApiRequests.create_order(authorized_user.token, order_body)
        assert response.status_code == 500
        assert ResponseMessage.INTERNAL_SERVER_ERROR in response.text
