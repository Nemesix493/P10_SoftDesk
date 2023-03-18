from rest_framework.exceptions import APIException
from rest_framework import status


class LoginRequired(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        'error': True,
        'message': "Login is required !"
    }
    default_code = 'not_authenticated'

    def __init__(self, link: str, detail=None, code=None):
        self.default_detail['login_endpoint'] = link
        super().__init__(detail, code)
    

class AccesDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        'error': True,
        'message': "Acces denied !"
    }
    default_code = 'acces_denied'


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        'error': True,
        'message': "Bad Request"
    }
    default_code = 'bad_request'
