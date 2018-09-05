from rest_framework.exceptions import APIException


class PhoneNumberInvalidAPIError(APIException):
    status_code = 400
    default_detail = 'Phone Number parameter was invalid'


class MonthInvalidAPIError(APIException):
    status_code = 400
    default_detail = 'Month parameter was invalid'
