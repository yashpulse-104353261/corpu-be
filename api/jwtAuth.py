import datetime
import time
import jwt

secret = "262CC47030B1803064844B94C1CB0054A247D1E550E26BB33F215149D8B2C72E"


def generate_auth_token(payload):

    iat = int(time.time())
    exp = int(time.time()) + 360000
    payload['iat'] = iat
    payload['exp'] = exp
    encoded_jwt = jwt.encode(payload,secret,algorithm="HS256")
    return encoded_jwt

def generate_refresh_token(payload):
    
    payload['token_type'] = "refresh"
    encoded_jwt = jwt.encode(payload,secret,algorithm="HS256")
    return encoded_jwt

def validate_auth_token(auth_token):
    
    try:
        payload = jwt.decode(auth_token,secret,algorithms=["HS256"])
        if payload['exp'] < int(time.time()):
            return False
        return payload
    except:
        return False
    
def validate_refresh_token(refresh_token):
    
    try:
        payload = jwt.decode(refresh_token,secret,algorithms=["HS256"])
        return payload
    except:
        return False