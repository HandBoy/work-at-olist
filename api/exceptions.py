from rest_framework.exceptions import APIException


class PhoneNumberInvalidAPI(APIException):
    status_code = 400
    default_detail = 'Phone Number parameter was invalid'
    

class MonthInvalidAPI(APIException):
    status_code = 400
    default_detail = 'Month parameter was invalid'
