
from django.http import QueryDict
from jwt         import decode

from api.config                   import SECRET_KEY
from rest_framework.response      import Response
from rest_framework.request       import Request
from rest_framework.decorators    import APIView

from routine.Log.Log              import Log
from routine.Model.Message        import Message
from routine.Model.Account        import Account
from routine.Model.Routine        import Routine
from routine.Model.RoutineDay     import RoutineDay
from routine.Model.RoutineResult  import RoutineResult
from routine.Serializer.Message   import MessageSerializer
from routine.Functions.ClearData  import isClearJWT, isClearRoutineListData
from routine.Functions.DateUtils  import DateConvertorToDate, getDateTimeByDay

"""
기간 검색 View

Request
[ /api/routines/?day=MON, GET ]
header: {
    "token": "j.w.t"
}
body: {}

Response
{
    "data" : [
        {
            "id": 2,
            "title": "test1",
            "result": "NOT",
            "category": "HOMEWORK",
            "is_alarm": true,
            "days": []
        },
        {
            "id": 3,
            "title": "test1",
            "result": "NOT",
            "category": "HOMEWORK",
            "is_alarm": true,
            "days": []
        }
    ],
    "message": {
        "msg": "목록 조회를 성공했습니다.", 
        "status": "ROUTINE_LIST_OK"
    }
}
"""
class RoutinesSearch(APIView):
    def get(self, request: Request):
        data    = request.GET
        jwt_str = request.META.get('HTTP_TOKEN')

        if type(data) == QueryDict:
            data = data.dict()

        # JWT 검증
        if not isClearJWT(jwt_str):
            Log.instance().error( "SEARCHs: ROUTINE_JWT_FAIL" )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_JWT_FAIL" ) ).data, status=400 )
        
        # header에 있는 JWT 꺼내기
        email     = decode(jwt_str, SECRET_KEY)["email"]
        account   = Account.objects.get( email = email )

        # 데이터 검증
        if not isClearRoutineListData(data, jwt_str):
            Log.instance().error( "SEARCHs: ROUTINE_LIST_FAIL", account.account_id )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_LIST_FAIL" ) ).data, status=400 )
        
        # 로그인 상태인지 확인
        if account.is_login == 0:
            Log.instance().error( "SEARCHs: ROUTINE_NOT_LOGIN", account.account_id )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_LIST_FAIL" ) ).data, status=400 )

        routine        = Routine.objects.filter( account = account, is_deleted = 0 ).select_related('account', 'category')
        routine_day    = RoutineDay.objects.filter( routine__in = routine, day = getDateTimeByDay( data["day"] ) ).select_related('routine')
        routine_result = RoutineResult.objects.filter( routine__in = routine_day.values("routine") ).select_related('routine', 'result').order_by('routine_id')

        serializer = []
        for result in routine_result:
            routine_days = RoutineDay.objects.filter( routine = result.routine ).select_related('routine')

            serializer.append({
                "id"       : result.routine.routine_id,
                "title"    : result.routine.title,
                "category" : result.routine.category.title,
                "result"   : result.result.title,
                "is_alarm" : True if result.routine.is_alarm == 1 else False,
                "days"     : DateConvertorToDate( routine_days )
            })

        Log.instance().info( "SEARCHs: ROUTINE_LIST_OK", account.account_id )
        return Response({
            "data":    serializer,
            "message": MessageSerializer(Message.getByCode( "ROUTINE_LIST_OK" )).data
        })