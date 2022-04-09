
from typing import Final

import jwt
from django.utils.timezone import now

from api.settings import SECRET_KEY

from rest_framework.response   import Response
from rest_framework.request    import Request
from rest_framework.decorators import api_view

from routine.Model.Message       import Message
from routine.Model.Account       import Account
from routine.Serializer.Message  import MessageSerializer
from routine.Functions.ClearData import isClearJWT

"""
로그아웃 View

Request
header: {
    "token": "j.w.t"
}
body: {}

Response
{
    "data":    { "account_id": 0 },
    "message": { "msg": ".", "status": "ROUTINE_LOGOUT_OK" }
}
"""
@api_view(['POST'])
def Logout(request: Request):
    jwt_str: Final = request.META.get('HTTP_TOKEN')

    # 데이터 검증
    if not isClearJWT(jwt_str):
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_LOGOUT_FAIL" ) ).data, status=400 )

    # 계정 정보 가져오기
    email   = jwt.decode(jwt_str, SECRET_KEY)["email"]
    account = Account.objects.get(email = email)

    # 이미 로그아웃이 되어있는지 확인
    if account.is_login == 0:
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_LOGOUT_FAIL" ) ).data, status=400 )

    # 로그아웃 정보 DB에 저장
    account.is_login = 0
    _now = now()
    account.logout_at, account.modified_at = _now, _now
    account.save()

    return Response({
        "data":    { "account_id": account.account_id },
        "message": MessageSerializer(Message.getByCode( "ROUTINE_LOGOUT_OK" )).data
    })