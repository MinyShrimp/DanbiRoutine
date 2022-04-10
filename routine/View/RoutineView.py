
from datetime import date, datetime
from typing   import Final
from jwt      import decode
from django.utils.timezone import now

from api.settings import SECRET_KEY

from rest_framework.response   import Response
from rest_framework.request    import Request
from rest_framework.decorators import APIView

from routine.Model.Account       import Account
from routine.Model.Message       import Message
from routine.Model.Category      import Category
from routine.Model.Result        import Result
from routine.Model.Routine       import Routine
from routine.Model.RoutineDay    import RoutineDay
from routine.Model.RoutineResult import RoutineResult
from routine.Serializer.Message  import MessageSerializer
from routine.Serializer.Routine  import RoutineIDSerializer
from routine.Functions.ClearData import isClearRoutineCreateData, isClearRoutineDeleteData, isClearRoutineDetailData

# /api/routine
class RoutineView(APIView):
    # SEARCH
    def get(self, request: Request):
        """
        Request:
        header: {
            "token": "j.w.t"
        }
        body: {
            "routine_id" : 3,
            "day": "2022-04-11"
        }

        Response:
        {
            "data": {
                "id": 4,
                "title": "test1",
                "result": "NOT"
            },
            "message": {
                "msg": "단건 조회를 성공했습니다.",
                "status": "ROUTINE_DETAIL_OK"
            }
        }
        """
        data:    Final = request.data
        jwt_str: Final = request.META.get('HTTP_TOKEN')

        # 데이터 검증
        if not isClearRoutineDetailData(data, jwt_str):
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_DETAIL_FAIL" ) ).data, status=400 )
        
        # header에 있는 JWT 꺼내기
        email     = decode(jwt_str, SECRET_KEY)["email"]
        account   = Account.objects.get( email = email )

        # 로그인 상태인지 확인
        if account.is_login == 0:
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_DETAIL_FAIL" ) ).data, status=400 )
        
        # body data 꺼내기
        routine_id = data["routine_id"]
        y, m, d    = data["day"].split('-')
        date       = datetime(int(y), int(m), int(d), 0, 0, 0, 0)

        routine        = Routine.objects.get( routine_id = routine_id, account = account, is_deleted = 0 )
        routine_result = RoutineResult.objects.get( routine = routine )
        routine_day    = RoutineDay.objects.get( routine = routine_result, day = date )

        routine_result_serializer = { 
            "id":     routine_day.routine.routine.routine_id,
            "title":  routine_day.routine.routine.title, 
            "result": routine_day.routine.result.title,
            "day":    routine_day.day
        }

        return Response({
            "data":    routine_result_serializer,
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
                "msg": " .", "status": "ROUTINE_CREATE_OK"
            }
        }
        """
        data:    Final = request.data
        jwt_str: Final = request.META.get('HTTP_TOKEN')

        # 데이터 검증
        if not isClearRoutineCreateData(data, jwt_str):
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_CREATE_FAIL" ) ).data, status=400 )

        # body 데이터 꺼내기
        title, category, goal, is_alarm, days = data["title"], data["category"], data["goal"], data["is_alarm"], data["days"]
        
        # header에 있는 JWT 꺼내기
        email     = decode(jwt_str, SECRET_KEY)["email"]
        account   = Account.objects.get( email = email )
        cateModel = Category.objects.get( title = category )

        # 로그인 상태인지 확인
        if account.is_login == 0:
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_CREATE_FAIL" ) ).data, status=400 )

        # Routine 생성
        routine = Routine.objects.create( 
            account = account, category = cateModel, title = title,
            is_alarm = 1 if is_alarm else 0, is_deleted = 0
        )

        routine_result = RoutineResult.objects.create(
            routine = routine, result = Result.objects.get(result_id = 1), is_deleted = 0
        )

        day_convertor = { "MON": 0, "TUE": 1, "WED": 2, "THR": 3, "FRI": 4, "SAT": 5, "SUN": 6 }
        _now = now()
        today = _now.weekday()
        for day in days:
            output, weekday = 0, day_convertor[day]

            if weekday >= today:
                output = weekday - today
            elif weekday < today:
                output = 7 - ( today - weekday )

            RoutineDay.objects.create(
                routine = routine_result, 
                day = date( _now.year, _now.month, _now.day + output )
            )

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
                "msg": " .", 
                "status": "ROUTINE_DELETE_OK"
            }
        }
        """
        data:    Final = request.data
        jwt_str: Final = request.META.get('HTTP_TOKEN')

        # 데이터 검증
        if not isClearRoutineDeleteData(data, jwt_str):
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_DELETE_FAIL" ) ).data, status=400 )
        
        # header에 있는 JWT 꺼내기
        email     = decode(jwt_str, SECRET_KEY)["email"]
        account   = Account.objects.get( email = email )

        # 로그인 상태인지 확인
        if account.is_login == 0:
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_DELETE_FAIL" ) ).data, status=400 )

        # body data 꺼내기
        routine_id = data["routine_id"]

        routine = Routine.objects.get(routine_id = routine_id)
        self.delete_model(routine)

        routine_result = RoutineResult.objects.get(routine_id = routine_id)
        self.delete_model(routine_result)

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
            "title"    : "(Optional)"
            "category" : "(Optional)",
            "goal"     : "(Optional)",
            "is_alarm" : "(Optional)",
            "days"     : (Optional)
        }

        Response:
        {
            "data": {
                "routine_id": 1
            },
            "message": {
                "msg": "성공적으로 업데이트되었습니다.", "status": "ROUTINE_UPDATE_OK"
            }
        }
        """

        data:    Final = request.data
        jwt_str: Final = request.META.get('HTTP_TOKEN')


        return Response({
            "data":    "put",
            "message": MessageSerializer(Message.getByCode( "ROUTINE_UPDATE_OK" )).data
        })