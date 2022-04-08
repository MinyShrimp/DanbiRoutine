
import re
from typing import Final

from rest_framework_simplejwt.authentication import JWTAuthentication

from routine.Model.Category import Category

def CheckEmail(email: str) -> bool:
    regex: Final = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search( regex, email )

def CheckPwd(pwd: str) -> bool:
    regex: Final = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    return re.search( regex, pwd )

def CheckInjection(s: str) -> bool:
    regex: Final = '(ALTER|CREATE|DELETE|DROP|EXEC(UTE){0,1}|INSERT( +INTO){0,1}|MERGE|SELECT|UPDATE|UNION( +ALL){0,1})'
    if re.search( regex, s ):
        return True
    
    regex2: Final = '[\{\}\[\]\/?,;:|\)*~`^\-_+<>\#$%&\\\=\(\'\"]'
    if re.search( regex2, s ):
        return True
    
    return False

# 이메일 체크
def isClearEmail(data: object):
    keys = list( data.keys() )
    if not ( "email" in keys ):
        return False

    email: str = data["email"]

    if CheckInjection(email):
        return False

    if not CheckEmail(email):
        return False

    return True

# 페스워드 체크
def isClearPwd(data: object):
    keys = list( data.keys() )
    if not ( "pwd" in keys ):
        return False

    pwd: str = data["pwd"]

    if CheckInjection(pwd):
        return False

    if not CheckPwd(pwd):
        return False

    return True

# JWT 체크
def isClearJWT(data: str):
    if data == None:
        return False

    try:
        autho = str( JWTAuthentication().get_validated_token( data ) )
        return autho == data
    except:
        return False

# Signup & Login에서 사용
def isClearDataEmailPwd(data: object):
    if not isClearEmail(data):
        return False
    
    # if not isClearPwd(data):
    #     return False

    return True

def isClearRoutineCreateData(data: object, jwt: str):
    # 키 값이 정상적으로 왔는지
    keys = list( data.keys() )
    for _ in ["title", "category", "goal", "is_alarm", "days"]:
        if not ( _ in keys ):
            return False

    # 값들의 자료형이 잘 왔는지
    title, category, goal, is_alarm, days = data["title"], data["category"], data["goal"], data["is_alarm"], data["days"]
    for i, j in zip([title, category, goal, is_alarm, days], [str, str, str, bool, list]):
        if type(i) != j:
            return False
    
    for v in [title, category, goal]:
        if CheckInjection(v):
            return False

    # 카테고리들이 유효하게 있는지
    categorys = Category.objects.all()
    if not( category in map( lambda x: x.title,  categorys ) ):
        return False

    # days의 최대 길이가 7 초과인 경우    
    if len(days) > 7:
        return False
    
    # days에 중복된 값이 있는 경우
    if len(set(days)) != len(days):
        return False

    # days 에서 MON~SUN 외에 다른 문자가 들어있는 경우
    for v in days:
        if not ( v in ["MON", "TUE", "WED", "THU", "FRI", "SET", "SUN"] ):
            return False
    
    return True