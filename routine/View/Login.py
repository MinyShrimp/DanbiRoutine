
from typing import Final

from django.utils.timezone import now

from rest_framework.response      import Response
from rest_framework.request       import Request
from rest_framework.decorators    import api_view

from routine.Log.Log              import Log
from routine.Model.Message        import Message
from routine.Model.Account        import Account
from routine.Serializer.Message   import MessageSerializer
from routine.Functions.ClearData  import isClearLoginData
from routine.Functions.GetPwd     import GetPwd
from routine.Token.EmailToken     import EmailToken

"""
로그인 View

Request
{ "email": "ksk7584@gmail.com", "pwd": "qwer1234!" }

Response
{
    "data":    { "account_id": 0, "token": "a.b.c" },
    "message": { "msg": ".", "status": "ROUTINE_LOGIN_OK" }
}
"""
@api_view(['POST'])
def Login(request: Request):
    data: Final = request.data

    # 데이터 검증
    if not isClearLoginData(data):
        Log.instance().error( "LOGIN: ROUTINE_DATA_NOT_CLEAN" )
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_LOGIN_FAIL" ) ).data, status=400 )

    # 계정 정보 가져오기
    account = Account.objects.get(email = data["email"])
    email, pwd, salt = account.email, account.pwd, account.salt

    # 이미 로그인이 되어있는지 확인
    if account.is_login == 1:
        Log.instance().error( "LOGIN: ROUTINE_ALREADY_LOGIN" )
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_LOGIN_FAIL" ) ).data, status=400 )

    # 비밀번호 비교
    if GetPwd( data["pwd"].encode('ascii'), salt ) != pwd:
        Log.instance().error( "LOGIN: ROUTINE_LOGIN_MISMATCH_PWD" )
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_LOGIN_MISMATCH_PWD" ) ).data, status=400 )

    # JWT 생성
    refresh = EmailToken.getToken(email)
    access  = refresh.access_token

    # 로그인 정보 DB에 저장
    account.is_login = 1
    _now = now()
    account.login_at, account.modified_at = _now, _now
    account.save()

    Log.instance().info( "LOGIN: ROUTINE_LOGIN_OK", account.account_id )
    return Response({
        "data":    { "account_id": account.account_id, "access_token": str(access), "refresh_token": str(refresh) },
        "message": MessageSerializer(Message.getByCode( "ROUTINE_LOGIN_OK" )).data
    })