
from datetime import datetime
import re
from typing import Final

import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.settings import SECRET_KEY
from routine.Functions.DateUtils import getDateTimeByDay

from routine.Log.Log             import Log
from routine.Model.Account       import Account
from routine.Model.Category      import Category
from routine.Model.Routine       import Routine
from routine.Model.RoutineDay    import RoutineDay
from routine.Model.RoutineResult import RoutineResult

def CheckEmail(email: str) -> bool:
    regex: Final = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}([.]\w{2,3})?$'
    return re.search( regex, email )

def CheckPwd(pwd: str) -> bool:
    regex: Final = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    return re.search( regex, pwd )

def CheckInjection(s: str) -> bool:
    regex: Final = '(ALTER|CREATE|DELETE|DROP|EXEC(UTE){0,1}|INSERT( +INTO){0,1}|MERGE|SELECT|UPDATE|UNION( +ALL){0,1})'
    if re.search( regex, s ):
        return True
    
    regex2: Final = '[\{\}\[\]\/?,;:|\)*~`^\-+<>\#$%&\\\=\(\'\"]'
    if re.search( regex2, s ):
        return True
    
    return False

def CheckKeys( data: list, keys: list ) -> bool:
    for _ in keys:
        if not ( _ in data ):
            return False
    return True

def CheckTypes( data: list, types: list ) -> bool:
    for i, j in zip(data, types):
        if type(i) != j:
            return False
    return True

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
    except Exception as e:
        Log.instance().error("UNVAILD_TOKEN")
        return False

# Signup에서 사용
def isClearDataEmailPwd(data: object):
    if not isClearEmail(data):
        return False
    
    if not isClearPwd(data):
        return False
    
    # 키 값이 정상적으로 왔는지
    if not CheckKeys( list( data.keys() ), ["email", "pwd"] ):
        return False
    
    # 값들의 자료형이 잘 왔는지
    datas = data["email"], data["pwd"]
    if not CheckTypes( datas, [ str, str ] ):
        return False

    return True
 
# Login에서 사용
def isClearLoginData(data: object):
    if not isClearDataEmailPwd(data):
        return False
    
    try:
        Account.objects.get(email = data["email"])
    except Exception as e:
        Log.instance().error(e)
        return False

    return True

# CreateRoutine에서 사용
def isClearRoutineCreateData(data: object, jwt_str: str):
    # 키 값이 정상적으로 왔는지
    if not CheckKeys( 
        list( data.keys() ), 
        ["title", "category", "goal", "is_alarm", "days"] 
    ):
        Log.instance().error("CREATE: INVALID_KEYS", data)
        return False

    # 값들의 자료형이 잘 왔는지
    title, category, goal, is_alarm, days = data["title"], data["category"], data["goal"], data["is_alarm"], data["days"]
    if not CheckTypes( 
        [title, category, goal, is_alarm, days], 
        [str, str, str, bool, list] 
    ):
        Log.instance().error("CREATE: INVALID_VALUES", data)
        return False
    
    # SQL Injection Check
    for v in [title, category, goal]:
        if CheckInjection(v):
            Log.instance().error("CREATE: SQL_INJECTION", data)
            return False

    # 카테고리들이 유효하게 있는지
    categorys = Category.objects.all()
    if not( category in map( lambda x: x.title,  categorys ) ):
        Log.instance().error("CREATE: INVALID_CATEGORY", data)
        return False

    # days의 최대 길이가 7 초과인 경우 
    if len(days) > 7 or len(days) == 0:
        Log.instance().error("CREATE: INVALID_DAYS_LEN", data)
        return False
    
    # days에 중복된 값이 있는 경우
    if len(set(days)) != len(days):
        Log.instance().error("CREATE: OVERLAP_DAYS", data)
        return False

    # days 에서 MON~SUN 외에 다른 문자가 들어있는 경우
    for v in days:
        if not ( v in ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"] ):
            Log.instance().error("CREATE: INVALID_DAYS_VALUE", data)
            return False
    
    try:
        email = jwt.decode(jwt_str, SECRET_KEY)["email"]
        Account.objects.get( email = email )
        Category.objects.get( title = category )
    except Exception as e:
        Log.instance().error("CREATE: INVALID_DB", data, e)
        return False
    
    return True

# DeleteRoutine, SearchRoutine에서 사용
def isClearRoutineDetailData(data: object, jwt_str: str):
    # 키 값이 정상적으로 왔는지
    if not CheckKeys( list( data.keys() ), ["routine_id"] ):
        Log.instance().error("SEARCH_DELETE: INVALID_KEY", data)
        return False

    # 값들의 자료형이 잘 왔는지
    try:
        routine_id = int( data["routine_id"] )
    except Exception as e:
        Log.instance().error("SEARCH_DELETE: INVALID_VALUE_TYPE", data, e)
        return False
    
    try:
        email = jwt.decode(jwt_str, SECRET_KEY)["email"]
        account = Account.objects.get( email = email )

        routine        = Routine.objects.get( routine_id = routine_id, account = account, is_deleted = 0 )
        routine_result = RoutineResult.objects.get( routine = routine )
    except Exception as e:
        Log.instance().error("SEARCH_DELETE: INVALID_DB", data, e)
        return False
    
    return True

# SearchRoutines에서 사용
def isClearRoutineListData(data: object, jwt_str: str):
    # 키 값이 정상적으로 왔는지
    if not CheckKeys( list( data.keys() ), ["day"] ):
        Log.instance().error("SEACRH_LIST: INVALID_KEY", data)
        return False

    # 값들의 자료형이 잘 왔는지
    day = data["day"]
    if day == '':
        Log.instance().error("SEACRH_LIST: INVALID_VALUE_EMPTY", data)
        return False
    
    # days 에서 MON~SUN 외에 다른 문자가 들어있는 경우
    if not ( day in ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"] ):
        Log.instance().error("SEACRH_LIST: INVALID_DAYS_VALUE", data)
        return False
    
    try:
        email   = jwt.decode(jwt_str, SECRET_KEY)["email"]
        account = Account.objects.get( email = email )
        
        routine        = Routine.objects.filter( account = account, is_deleted = 0 )
        routine_day    = RoutineDay.objects.filter( routine__in = routine, day = getDateTimeByDay( day ) )
        routine_result = RoutineResult.objects.filter( routine__in = routine_day.values("routine") )
        if routine.exists() == None or routine_day.exists() == None or routine_result.exists() == None:
            Log.instance().error("SEACRH_LIST: INVALID_DB", data)
            return False

    except Exception as e:
        Log.instance().error("SEACRH_LIST: INVALID_DB", data, e)
        return False
    
    return True

# UpdateRoutine에서 사용
def isClearRoutineUpdateData(data: object, jwt_str: str):
    # 키 값이 정상적으로 왔는지
    if not CheckKeys( 
        list( data.keys() ), 
        ["routine_id", "title", "category", "goal", "is_alarm", "days"]
    ):
        Log.instance().error("UPDATE: INVALID_KEY", data)
        return False

    # 값들의 자료형이 잘 왔는지
    routine_id, title, category, goal, is_alarm, days = \
        data["routine_id"], data["title"], data["category"], data["goal"], data["is_alarm"], data["days"]
    if not CheckTypes( 
        [routine_id, title, category, goal, is_alarm, days], 
        [int, str, str, str, bool, list] 
    ):
        Log.instance().error("UPDATE: INVALID_VALUE_TYPE", data)
        return False

    # SQL Injection Check
    for v in [title, category, goal]:
        if CheckInjection(v):
            Log.instance().error("UPDATE: SQL_INJECTION", data)
            return False

    # 카테고리들이 유효하게 있는지
    categorys = Category.objects.all()
    if not( category in map( lambda x: x.title,  categorys ) ):
        Log.instance().error("UPDATE: INVALID_CATEGORY", data)
        return False

    # days의 최대 길이가 7 초과인 경우    
    if len(days) > 7 or len(days) == 0:
        Log.instance().error("UPDATE: INVALID_DAYS_LEN", data)
        return False
    
    # days에 중복된 값이 있는 경우
    if len(set(days)) != len(days):
        Log.instance().error("UPDATE: INVALID_DAYS_LEN", data)
        return False

    # days 에서 MON~SUN 외에 다른 문자가 들어있는 경우
    for v in days:
        if not ( v in ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"] ):
            Log.instance().error("UPDATE: INVALID_DAYS_VALUE", data)
            return False
    
    try:
        email   = jwt.decode(jwt_str, SECRET_KEY)["email"]
        account = Account.objects.get( email = email )

        Routine.objects.select_related('account', 'category').get( routine_id = routine_id, account = account, is_deleted = 0 )
    except Exception as e:
        Log.instance().error("UPDATE: INVALID_DB", data, e)
        return False
    
    return True

# RoutineResultView 에서 사용
def isClearRoutineResultData(data: object, jwt_str: str):
    # 키 값이 정상적으로 왔는지
    if not CheckKeys( 
        list( data.keys() ), 
        ["routine_id", "result"]
    ):
        Log.instance().error("RESULT: INVALID_KEY", data)
        return False

    # 값들의 자료형이 잘 왔는지
    routine_id, result = data["routine_id"], data["result"]
    if not CheckTypes( 
        [routine_id, result], 
        [int, str] 
    ):
        Log.instance().error("RESULT: INVALID_VALUE_TYPE", data)
        return False

    # SQL Injection Check
    if CheckInjection(result):
        Log.instance().error("RESULT: SQL_INJECTION", data)
        return False
    
    # result 에서 NOT, TRY, DONE 외에 다른 문자가 들어있는 경우
    if not ( result in ["NOT", "TRY", "DONE"] ):
        Log.instance().error("RESULT: INVALID_DAYS_VALUE", data)
        return False
    
    try:
        email   = jwt.decode(jwt_str, SECRET_KEY)["email"]
        account = Account.objects.get( email = email )

        routine        = Routine.objects.select_related('account', 'category').get( routine_id = routine_id, account = account, is_deleted = 0 )
        routine_result = RoutineResult.objects.select_related('routine', 'result').get( routine = routine, is_deleted = 0 )
    except Exception as e:
        Log.instance().error("UPDATE: INVALID_DB", data, e)
        return False
    
    return True