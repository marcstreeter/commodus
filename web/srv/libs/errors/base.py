class BaseError(Exception):
    """
    all errors inherit from this error
    other than establishing general behaviour
    it it not meant to be raised as it does not
    have any default `_err_xxxxxx` set up
    of error
    """
    __slots__ = (
        '_err_reason',
        '_err_message',
        '_err_code',
        '_err_category'
    )

    def __init__(self, reason=None, code=None, message=None):
        if reason is not None:
            self._err_reason = str(reason)

        if code is not None:
            self._err_code = int(code)

        if message is not None:
            self._err_message = str(message)

    def __str__(self):
        return f"({self.code} | {self.reason}){self.message}"

    @property
    def code(self) -> int:
        """
        HTTP status code
        """
        return self._err_code

    @property
    def message(self) -> str:
        """
        error description only visible via logging
        """
        return self._err_message

    @property
    def log_message(self) -> str:
        """
        conveniently mimics tornado HTTPError
        """
        return self._err_message

    @property
    def reason(self) -> str:
        """
        error description exposed via api to public
        """
        return self._err_reason

    @property
    def category(self) -> str:
        """
        generalized theme of error
        NOTE: never meant to be modified
        """
        try:
            return self._err_category
        except:
            return 'UNCATEGORIZED'

class CommodusErrors(BaseError):
    _err_reason = "unknown error"
    _err_message = "unknown error"
    _err_category = "COMMODUS"
    _err_code = 500