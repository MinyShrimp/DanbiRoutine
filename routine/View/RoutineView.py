
from datetime import date
from typing import Final
import jwt
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
from routine.Serializer.Routine  import RoutineIDSerializer, RoutineResultSerializer
from routine.Functions.ClearData import isClearRoutineCreateData, isClearRoutineDeleteData

# /api/routine
class RoutineView(APIView):
    """ """
    """
    Request:
    header: {
        "token": "j.w.t"
    }
    body: {
        "routine_id" : 3
    }

    Response:
    {
        "data" : {
            "goal" : " 2 ",
            "id" : 1,
            "result" : "NOT",
            "title" : " !"
        },
        "message": { "msg": " .", "status": "ROUTINE_DETAIL_OK" }
    }
    """
    # SEARCH
    def get(self, request: Request):
        data:    Final = request.data
        jwt_str: Final = request.META.get('HTTP_TOKEN')

        # 데이터 검증
        if not isClearRoutineDeleteData(data, jwt_str):
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_DETAIL_FAIL" ) ).data, status=400 )
        
        # header에 있는 JWT 꺼내기
        email     = jwt.decode(jwt_str, SECRET_KEY)["email"]
        account   = Account.objects.get( email = email )

        # 로그인 상태인지 확인
        if account.is_login == 0:
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_DETAIL_FAIL" ) ).data, status=400 )
        
        # body data 꺼내기
        routine_id = data["routine_id"]

        routine = Routine.objects.get(routine_id = routine_id)
        routine_result = RoutineResult.objects.get( is_deleted = 0, routine = routine )

        return Response({
            "data":    RoutineResultSerializer(routine_result).data,
            "message": MessageSerializer(Message.getByCode( "ROUTINE_DETAIL_OK" )).data
        })

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
    # CREATE
    def post(self, request: Request):
        data:    Final = request.data
        jwt_str: Final = request.META.get('HTTP_TOKEN')

        # 데이터 검증
        if not isClearRoutineCreateData(data, jwt_str):
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_CREATE_FAIL" ) ).data, status=400 )

        # body 데이터 꺼내기
        title, category, goal, is_alarm, days = data["title"], data["category"], data["goal"], data["is_alarm"], data["days"]
        
        # header에 있는 JWT 꺼내기
        email     = jwt.decode(jwt_str, SECRET_KEY)["email"]
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
                routine = routine, 
                day = date( _now.year, _now.month, _now.day + output )
            )

        RoutineResult.objects.create(
            routine = routine, result = Result.objects.get(result_id = 1), is_deleted = 0
        )

        return Response({
            "data":    RoutineIDSerializer(routine).data,
            "message": MessageSerializer(Message.getByCode( "ROUTINE_CREATE_OK" )).data
        })

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
    # DELETE
    def delete_model(self, model):
        model.is_deleted, model.modified_at = 1, now()
        model.save()

    def delete(self, request: Request):
        data:    Final = request.data
        jwt_str: Final = request.META.get('HTTP_TOKEN')

        # 데이터 검증
        if not isClearRoutineDeleteData(data, jwt_str):
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_DELETE_FAIL" ) ).data, status=400 )
        
        # header에 있는 JWT 꺼내기
        email     = jwt.decode(jwt_str, SECRET_KEY)["email"]
        account   = Account.objects.get( email = email )

        # 로그인 상태인지 확인
        if account.is_login == 0:
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_CREATE_FAIL" ) ).data, status=400 )

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
            "msg": " .", "status": "ROUTINE_UPDATE_OK"
        }
    }
    """
    # Update
    def put(self, request: Request):
        return Response("put")