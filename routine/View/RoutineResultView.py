
from typing   import Final
from jwt      import decode

from api.config                   import SECRET_KEY
from rest_framework.response      import Response
from rest_framework.request       import Request
from rest_framework.decorators    import APIView

from routine.Log.Log              import Log
from routine.Model.Message        import Message
from routine.Model.Account        import Account
from routine.Model.Result         import Result
from routine.Model.Routine        import Routine
from routine.Model.RoutineResult  import RoutineResult
from routine.Serializer.Message   import MessageSerializer
from routine.Functions.ClearData  import isClearJWT, isClearRoutineResultData

"""
Request
[/api/result/, put]
header: {
    "token": "j.w.t"
}
body: {
    "routine_id" : 5,
    "result"     : "TRY"
}

Response
{
    "data": {
        "routine_id": 5,
        "result" : "TRY"
    },
    "message": {
        "msg": "성공적으로 결과를 업데이트되었습니다.", 
        "status": "ROUTINE_RESULT_OK"
    }
}
"""
class RoutineResultView(APIView):
    def put(self, request: Request):
        data:    Final = request.data
        jwt_str: Final = request.META.get('HTTP_TOKEN')

        # JWT 검증
        if not isClearJWT(jwt_str):
            Log.instance().error( "RESULT: ROUTINE_JWT_FAIL" )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_JWT_FAIL" ) ).data, status=400 )
        
        # header에 있는 JWT 꺼내기
        email     = decode(jwt_str, SECRET_KEY)["email"]
        account   = Account.objects.get( email = email )

        # 데이터 검증
        if not isClearRoutineResultData(data, jwt_str):
            Log.instance().error( "RESULT: ROUTINE_RESULT_FAIL", account.account_id )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_RESULT_FAIL" ) ).data, status=400 )

        # 로그인 상태인지 확인
        if account.is_login == 0:
            Log.instance().error( "RESULT: ROUTINE_NOT_LOGIN", account.account_id )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_RESULT_FAIL" ) ).data, status=400 )

        # body 데이터 꺼내기
        routine_id, result = data["routine_id"], data["result"]
        
        routine        = Routine.objects.select_related('account', 'category').get( routine_id = routine_id, account = account, is_deleted = 0 )
        routine_result = RoutineResult.objects.select_related('routine', 'result').get( routine = routine, is_deleted = 0 )

        routine_result.result = Result.objects.get( title = result )
        routine_result.save()

        serializer = {
            "routine_id" : routine.routine_id,
            "result"     : routine_result.result.title
        }

        Log.instance().info( "RESULT: ROUTINE_RESULT_OK", account.account_id, routine.routine_id )
        return Response({
            "data":    serializer,
            "message": MessageSerializer(Message.getByCode( "ROUTINE_RESULT_OK" )).data
        })