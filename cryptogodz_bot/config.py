import os

from .exceptions import ParameterNotFound, InvalidParameter

class Conf:

    def __init__(self):
        self.WALLET = os.getenv('WALLET')
        self.MAX_BNB_FEE = os.getenv('MAX_BNB_FEE')
        self.UMBRA_LEVEL = os.getenv('UMBRA_LEVEL')
        self.WEBDRIVER_PATH = os.getenv('WEBDRIVER_PATH')
        self.EXTENSION_PATH = os.getenv('EXTENSION_PATH')
        self.TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        self.SECRET_RECOVERY_PHRASE = os.getenv('SECRET_RECOVERY_PHRASE')
        self.NODE_API_URL = os.getenv('NODE_API_URL')
        self.check_string_variables()
        self.check_numeric_variables()

    def check_string_variables(self):
        if self.WALLET is None:
            raise ParameterNotFound("Parameter WALLET not found.")
        if self.WEBDRIVER_PATH is None:
            raise ParameterNotFound("Parameter WEBDRIVER_PATH not found.")
        if self.EXTENSION_PATH is None:
            raise ParameterNotFound("Parameter EXTENSION_PATH not found.")
        if self.TELEGRAM_CHAT_ID is None:
            raise ParameterNotFound("Parameter TELEGRAM_CHAT_ID not found.")
        if self.TELEGRAM_TOKEN is None:
            raise ParameterNotFound("Parameter TELEGRAM_TOKEN not found.")
        if self.SECRET_RECOVERY_PHRASE is None:
            raise ParameterNotFound("Parameter SECRET_RECOVERY_PHRASE not found.")
        if self.NODE_API_URL is None:
            raise ParameterNotFound("Parameter NODE_API_URL not found.")

    def check_numeric_variables(self):
        if self.MAX_BNB_FEE is None:
            raise ParameterNotFound("Parameter MAX_BNB_FEE not found.")
        try:
            self.MAX_BNB_FEE = float(self.MAX_BNB_FEE)
        except:
            raise InvalidParameter("Parameter MAX_BNB_FEE is not a valid float.")
        if self.UMBRA_LEVEL is None:
            raise ParameterNotFound("Parameter UMBRA_LEVEL not found.")
        elif self.UMBRA_LEVEL.isdigit() is False:
            raise InvalidParameter("Parameter UMBRA_LEVEL is not a valid integer.")
        elif self.UMBRA_LEVEL < 1 or self.UMBRA_LEVEL > 30:
            raise InvalidParameter("Parameter UMBRA_LEVEL must be an integer between [1, 30].")
