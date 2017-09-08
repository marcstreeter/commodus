from .base import CommodusErrors


class GeneralErrors(CommodusErrors):
    _err_category = "GENERAL"
    _err_code = 500
    _err_message = "general error"
    _err_reason = "general error"

class InvalidRequest(GeneralErrors):
    _err_message = "invalid request"
    _err_code = 400