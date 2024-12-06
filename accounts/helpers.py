from django.utils.crypto import get_random_string

def generateOTP(length=6):
    allowed_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return get_random_string(length=length, allowed_chars=allowed_chars)
