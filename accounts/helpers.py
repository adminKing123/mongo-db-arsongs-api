from django.utils.crypto import get_random_string
from config import CONFIG

def generateOTP(length=None):
    length = length or CONFIG["OTP_LENGTH"]
    return get_random_string(length=length, allowed_chars=CONFIG["OTP_ALLOWED_CHARS"])
