import os
from typing import Final

from rest_framework.response   import Response
from rest_framework.request    import Request
from rest_framework.decorators import api_view

from routine.Model.Message                import Message
from routine.Model.Account                import Account
from routine.Serializer.MessageSerializer import MessageSerializer
from routine.Serializer.AccountSerializer import AccountIDSerializer
from routine.Verification.ClearData       import isClearDataEmailPwd
from routine.Verification.GetPwd          import GetPwd

"""
회원가입 View

Request
{ "email": "ksk7584@gmail.com", "pwd": "qwer1234!" }

Response
{
    "data":    { "account_id": 0 },
    "message": { "msg": ".", "status": "ROUTINE_SIGNUP_OK" }
}
"""
@api_view(['POST'])
def SignUp(request: Request):
    data: Final = request.data

    # 데이터 검증
    if not isClearDataEmailPwd(data):
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_SIGNUP_FAIL" ) ).data, status=400 )
    
    # Email 중복체크
    if Account.objects.filter(email=data['email']).exists():
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_SIGNUP_EMAIL_OVERLAP" ) ).data, status=400 )
    
    # pwd => SHA-512 암호화
    # salt => 랜덤 시드
    # ( salt + pwd ) 를 SHA-512 암호화 * 3
    email = data['email']
    salt  = os.urandom(16)
    pwd   = GetPwd( data['pwd'].encode('ascii'), salt )

    # Insert Account
    account = Account.objects.create(email=email, pwd=pwd, salt=salt)
    
    return Response({
        "data":    AccountIDSerializer(account).data,
        "message": MessageSerializer(Message.getByCode( "ROUTINE_SIGNUP_OK" )).data
    })