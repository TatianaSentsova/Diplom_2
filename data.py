class Url:
    STELLAR_BURGERS_URL = 'https://stellarburgers.nomoreparties.site/'
    ENDPOINT_USER = '/api/auth/register'
    ENDPOINT_LOGIN = '/api/auth/login'
    ENDPOINT_DELETE_USER = '/api/auth/user'


class ResponseMessage:
    USER_ALREADY_EXISTS = {"success": False,
                           "message": "User already exists"}
    NOT_ENOUGH_DATA_FOR_CREATE = {"success": False,
                                  "message": "Email, password and name are required fields"}
    EMAIL_OR_PASSWORD_ARE_INCORRECT = {"success": False,
                                       "message": "email or password are incorrect"}