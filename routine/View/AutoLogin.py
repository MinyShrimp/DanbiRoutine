
from typing import Final

import jwt
from django.utils.timezone import now

from api.settings import SECRET_KEY

from rest_framework.response      import Response
from rest_framework.request       import Request
from rest_framework.decorators    import api_view

from routine.Log.Log              import Log
from routine.Model.Message        import Message
from routine.Model.Account        import Account
from routine.Serializer.Message   import MessageSerializer
from routine.Functions.ClearData  import isClearJWT

"""
Auto로그인 View

Request
headers: {
    token: "j.w.t"
}
body: {}

Response
{
    "data":    { "account_id": 0, "token": "a.b.c" },
    "message": { "msg": ".", "status": "ROUTINE_LOGIN_OK" }
}
"""
@api_view(['POST'])
def AutoLogin(request: Request):
    jwt_str: Final = request.META.get('HTTP_TOKEN')

    # 데이터 검증
    if not isClearJWT(jwt_str):
        Log.instance().error( "AUTO_LOGIN: ROUTINE_DATA_NOT_CLEAN" )
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_LOGIN_FAIL" ) ).data, status=400 )

    # 계정 정보 가져오기
    email   = jwt.decode(jwt_str, SECRET_KEY)["email"]
    account = Account.objects.get(email = email)

    # 이미 로그아웃이 되어있는지 확인
    if account.is_login == 0:
        Log.instance().error( "AUTO_LOGIN: ROUTINE_ALREADY_LOGIN", account.account_id )
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_LOGIN_FAIL" ) ).data, status=400 )

    # 로그인 정보 DB에 저장
    _now = now()
    account.login_at, account.modified_at = _now, _now
    account.save()

    Log.instance().info( "AUTO_LOGIN: ROUTINE_LOGIN_OK", account.account_id )
    return Response({
        "data":    { "account_id": account.account_id },
        "message": MessageSerializer(Message.getByCode( "ROUTINE_LOGIN_OK" )).data
    })