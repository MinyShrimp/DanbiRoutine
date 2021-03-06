
from typing   import Final
from jwt      import decode

from django.http import QueryDict
from django.utils.timezone import now

from api.settings import SECRET_KEY

from rest_framework.response   import Response
from rest_framework.request    import Request
from rest_framework.decorators import APIView

from routine.Log.Log             import Log
from routine.Model.Account       import Account
from routine.Model.Message       import Message
from routine.Model.Category      import Category
from routine.Model.Result        import Result
from routine.Model.Routine       import Routine
from routine.Model.RoutineDay    import RoutineDay
from routine.Model.RoutineResult import RoutineResult
from routine.Serializer.Message  import MessageSerializer
from routine.Serializer.Routine  import RoutineIDSerializer
from routine.Functions.ClearData import isClearJWT, isClearRoutineCreateData, isClearRoutineDetailData, isClearRoutineUpdateData
from routine.Functions.DateUtils import DateConvertor, DateConvertorToDate, getDateTimeMon, getDateTimeSun

# /api/routine
class RoutineView(APIView):
    # SEARCH
    def get(self, request: Request):
        """
        [ /api/routine/?routine_id=3, GET ]
        Request:
        header: {
            "token": "j.w.t"
        }
        body: {}

        Response:
        {
            "data": {
                "id": 3,
                "title": "test1",
                "result": "NOT",
                "category": "HOMEWORK",
                "is_alarm": true,
                "days": []
            },
            "message": {
                "msg": "단건 조회를 성공했습니다.",
                "status": "ROUTINE_DETAIL_OK"
            }
        }
        """
        data    = request.GET
        jwt_str = request.META.get('HTTP_TOKEN')

        if type(data) == QueryDict:
            data = data.dict()

        # JWT 검증
        if not isClearJWT(jwt_str):
            Log.instance().error( "SEARCH: ROUTINE_JWT_FAIL" )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_JWT_FAIL" ) ).data, status=400 )

        # header에 있는 JWT 꺼내기
        email     = decode(jwt_str, SECRET_KEY)["email"]
        account   = Account.objects.get( email = email )

        # 데이터 검증
        if not isClearRoutineDetailData(data, jwt_str):
            Log.instance().error( "SEARCH: ROUTINE_DETAIL_FAIL", account.account_id )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_DETAIL_FAIL" ) ).data, status=400 )

        # 로그인 상태인지 확인
        if account.is_login == 0:
            Log.instance().error( "SEARCH: ROUTINE_NOT_LOGIN", account.account_id )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_DETAIL_FAIL" ) ).data, status=400 )
        
        # body data 꺼내기
        routine_id = data["routine_id"]

        monday, sunday = getDateTimeMon(), getDateTimeSun()

        routine        = Routine.objects.select_related('account', 'category').get( routine_id = routine_id, account = account, is_deleted = 0 )
        routine_result = RoutineResult.objects.select_related('routine', 'result').get( routine = routine )
        routine_day    = RoutineDay.objects.filter( routine = routine, day__range = ( monday, sunday ) ).select_related('routine')

        routine_serializer = {
            "id"       : routine.routine_id,
            "title"    : routine.title,
            "category" : routine.category.title,
            "result"   : routine_result.result.title,
            "is_alarm" : True if routine.is_alarm == 1 else False,
            "days"     : DateConvertorToDate(routine_day)
        }

        Log.instance().info( "SEARCH: ROUTINE_DETAIL_OK", account.account_id, routine.routine_id )
        return Response({
            "data":    routine_serializer,
            "message": MessageSerializer(Message.getByCode( "ROUTINE_DETAIL_OK" )).data
        })

    # CREATE
    def post(self, request: Request):
        """
        Request:
        header: {
            "token": "j.w.t"
        }
        body: {
            "title": "",
            "category": "HOMEWORK",
            "goal": "",
            "is_alarm": true,
            "days": ["MON", "WED", "FRI"]
        }

        Response:
        {
            "data": {
                "routine_id": 1
            },
            "message": {
                "msg": "성공적으로 생성되었습니다.", 
                "status": "ROUTINE_CREATE_OK"
            }
        }
        """
        data:    Final = request.data
        jwt_str: Final = request.META.get('HTTP_TOKEN')

        # JWT 검증
        if not isClearJWT(jwt_str):
            Log.instance().error( "CREATE: ROUTINE_JWT_FAIL" )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_JWT_FAIL" ) ).data, status=400 )

        # header에 있는 JWT 꺼내기
        email     = decode(jwt_str, SECRET_KEY)["email"]
        account   = Account.objects.get( email = email )

        # 데이터 검증
        if not isClearRoutineCreateData(data, jwt_str):
            Log.instance().error( "CREATE: ROUTINE_CREATE_FAIL", account.account_id )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_CREATE_FAIL" ) ).data, status=400 )

        # 로그인 상태인지 확인
        if account.is_login == 0:
            Log.instance().error( "CREATE: ROUTINE_NOT_LOGIN", account.account_id )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_CREATE_FAIL" ) ).data, status=400 )

        # body 데이터 꺼내기
        title, category, goal, is_alarm, days = data["title"], data["category"], data["goal"], data["is_alarm"], data["days"]
        cateModel = Category.objects.get( title = category )

        # Routine 생성
        routine = Routine.objects.select_related('account', 'category').create( 
            account = account, category = cateModel, title = title,
            is_alarm = 1 if is_alarm else 0, is_deleted = 0
        )

        RoutineResult.objects.create(
            routine = routine, result = Result.objects.get(title = "NOT"), is_deleted = 0
        )
        
        RoutineDay.objects.bulk_create(
            [ RoutineDay( routine = routine, day = _day ) for _day in DateConvertor(days) ]
        )

        Log.instance().info( "CREATE: ROUTINE_CREATE_OK", account.account_id, routine.routine_id )
        return Response({
            "data":    RoutineIDSerializer(routine).data,
            "message": MessageSerializer(Message.getByCode( "ROUTINE_CREATE_OK" )).data
        })

    # DELETE
    def delete_model(self, model):
        model.is_deleted, model.modified_at = 1, now()
        model.save()

    def delete(self, request: Request):
        """
        Request:
        header: {
            "token": "j.w.t"
        }
        body: {
            "routine_id" : 1
        }

        Response:
        {
            "data": {
                "routine_id": 1
            },
            "message": {
                "msg": "성공적으로 삭제되었습니다.", 
                "status": "ROUTINE_DELETE_OK"
            }
        }
        """
        data:    Final = request.data
        jwt_str: Final = request.META.get('HTTP_TOKEN')

        # JWT 검증
        if not isClearJWT(jwt_str):
            Log.instance().error( "DELETE: ROUTINE_JWT_FAIL" )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_JWT_FAIL" ) ).data, status=400 )
        
        # header에 있는 JWT 꺼내기
        email     = decode(jwt_str, SECRET_KEY)["email"]
        account   = Account.objects.get( email = email )

        # 데이터 검증
        if not isClearRoutineDetailData(data, jwt_str):
            Log.instance().error( "DELETE: ROUTINE_DELETE_FAIL", account.account_id )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_DELETE_FAIL" ) ).data, status=400 )
        
        # 로그인 상태인지 확인
        if account.is_login == 0:
            Log.instance().error( "DELETE: ROUTINE_NOT_LOGIN", account.account_id )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_DELETE_FAIL" ) ).data, status=400 )

        # body data 꺼내기
        routine_id = data["routine_id"]

        routine = Routine.objects.select_related('account', 'category').get( routine_id = routine_id )
        self.delete_model(routine)

        routine_result = RoutineResult.objects.get( routine = routine )
        self.delete_model(routine_result)

        RoutineDay.objects.filter( routine = routine ).delete()

        Log.instance().info( "DELETE: ROUTINE_DELETE_OK", account.account_id, routine.routine_id )
        return Response({
            "data":    RoutineIDSerializer(routine).data,
            "message": MessageSerializer(Message.getByCode( "ROUTINE_DELETE_OK" )).data
        })

    # Update
    def put(self, request: Request):
        """
        Request:
        header: {
            "token": "j.w.t"
        }
        body: {
            "routine_id" : 5,
            "title"      : "test1",
            "category"   : "HOMEWORK",
            "goal"       : "test2",
            "is_alarm"   : true,
            "days"       : [ "MON" ]
        }

        Response:
        {
            "data": {
                "routine_id": 1
            },
            "message": {
                "msg": "성공적으로 업데이트되었습니다.", 
                "status": "ROUTINE_UPDATE_OK"
            }
        }
        """

        data:    Final = request.data
        jwt_str: Final = request.META.get('HTTP_TOKEN')

        # JWT 검증
        if not isClearJWT(jwt_str):
            Log.instance().error( "UPDATE: ROUTINE_JWT_FAIL" )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_JWT_FAIL" ) ).data, status=400 )

        # header에 있는 JWT 꺼내기
        email     = decode(jwt_str, SECRET_KEY)["email"]
        account   = Account.objects.get( email = email )

        # 데이터 검증
        if not isClearRoutineUpdateData(data, jwt_str):
            Log.instance().error( "UPDATE: ROUTINE_UPDATE_FAIL", account.account_id )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_UPDATE_FAIL" ) ).data, status=400 )
            
        # 로그인 상태인지 확인
        if account.is_login == 0:
            Log.instance().error( "UPDATE: ROUTINE_NOT_LOGIN", account.account_id )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_UPDATE_FAIL" ) ).data, status=400 )

        # body data 꺼내기
        routine_id, title, category, goal, is_alarm, days = \
            data["routine_id"], data["title"], data["category"], data["goal"], data["is_alarm"], data["days"]

        routine = Routine.objects.select_related('account', 'category').get( routine_id = routine_id, account = account, is_deleted = 0 )
        routine_days = RoutineDay.objects.filter( routine = routine ).select_related('routine')

        routine.title       = title
        routine.category    = Category.objects.get( title = category )
        routine.is_alarm    = 1 if is_alarm else 0
        routine.modified_at = now()
        routine.save()

        routine_days.delete()
        RoutineDay.objects.bulk_create(
            [ RoutineDay( routine = routine, day = _day ) for _day in DateConvertor(days) ]
        )

        Log.instance().info( "UPDATE: ROUTINE_UPDATE_OK", account.account_id, routine.routine_id )
        return Response({
            "data":    RoutineIDSerializer(routine).data,
            "message": MessageSerializer(Message.getByCode( "ROUTINE_UPDATE_OK" )).data
        })