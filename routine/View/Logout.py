
from datetime import datetime
from typing import Final

from rest_framework.response   import Response
from rest_framework.request    import Request
from rest_framework.decorators import api_view

from routine.Model.Message                import Message
from routine.Model.Account                import Account
from routine.Serializer.MessageSerializer import MessageSerializer
from routine.Verification.ClearData       import isClearLogoutData

"""
로그아웃 View

Request
{ "email": "ksk7584@gmail.com", "jwt": "a.b.c" }

Response
{
    "data":    { "account_id": 0 },
    "message": { "msg": ".", "status": "ROUTINE_LOGOUT_OK" }
}
"""
@api_view(['POST'])
def Logout(request: Request):
    data: Final = request.data

    # 데이터 검증
    if not isClearLogoutData(data):
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_LOGOUT_FAIL" ) ).data, status=400 )

    # 계정 정보 가져오기
    account = Account.objects.get(email = data["email"])

    # 이미 로그아웃이 되어있는지 확인
    if account.is_login == 0:
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_LOGOUT_FAIL" ) ).data, status=400 )

    # 로그아웃 정보 DB에 저장
    account.is_login = 0
    account.logout_at = datetime.now()
    account.save()

    return Response({
        "data":    { "account_id": account.account_id },
        "message": MessageSerializer(Message.getByCode( "ROUTINE_LOGOUT_OK" )).data
    })