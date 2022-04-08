
import re
from typing import Final

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken

def CheckEmail(email: str) -> bool:
    regex: Final = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search( regex, email )

def CheckPwd(pwd: str) -> bool:
    regex: Final = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    return re.search( regex, pwd )

# 이메일 체크
def isClearEmail(data: object):
    keys = list( data.keys() )
    if not ( "email" in keys ):
        return False

    email: str = data["email"]

    if not CheckEmail(email):
        return False

    return True

# 페스워드 체크
def isClearPwd(data: object):
    keys = list( data.keys() )
    if not ( "pwd" in keys ):
        return False

    pwd: str = data["pwd"]

    if not CheckPwd(pwd):
        return False

    return True

# JWT 체크
def isClearJWT(data: object):
    keys = list( data.keys() )
    if not ( "jwt" in keys ):
        return False

    jwt: str = data["jwt"]

    try:
        autho = str( JWTAuthentication().get_validated_token( jwt ) )
        return autho == jwt
    except:
        return False

# Signup & Login에서 사용
def isClearDataEmailPwd(data: object):
    if not isClearEmail(data):
        return False
    
    if not isClearPwd(data):
        return False

    return True

# Logout에서 사용
def isClearLogoutData(data: object):
    if not isClearEmail(data):
        return False
    
    if not isClearJWT(data):
        return False

    return True