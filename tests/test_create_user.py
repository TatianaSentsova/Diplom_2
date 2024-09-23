import pytest
import allure
from api_shop import ApiRequests, ApiBodyBuilder
from data import ResponseMessage
from fake_data import FakeData


class TestCreatingCourier:
    @allure.title("Успешное создание пользователя при заполнении всех полей")
    def test_creating_new_courier(self, request_user_body):
        response = ApiRequests.create_user(request_user_body)
        assert response.status_code == 200
        assert response.json()['success']

    @allure.title("Невозможно создать пользователя, который уже зарегистрирован")
    def test_creating_same_user(self, request_user_body):
        ApiRequests.create_user(request_user_body)
        response = ApiRequests.create_user(request_user_body)
        assert response.status_code == 403
        assert response.json() == ResponseMessage.USER_ALREADY_EXISTS

    @allure.title("Нельзя создать пользователя, не заполнив одно из обязательных полей")
    @pytest.mark.parametrize('email, password, name', [['', FakeData.password(), FakeData.name()],
                                                       [FakeData.email(), '', FakeData.name()],
                                                       [FakeData.email(), FakeData.password(), '']])
    def test_creating_user_without_required_field(self, email, password, name):
        body_user = ApiBodyBuilder.build_user_body(email, password, name)
        response = ApiRequests.create_user(body_user)
        assert response.status_code == 403
        assert response.json() == ResponseMessage.NOT_ENOUGH_DATA_FOR_CREATE
