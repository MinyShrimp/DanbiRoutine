
from datetime import datetime, date
from typing import Final
import jwt, pytz
from django.utils import timezone

from api.settings import SECRET_KEY

from rest_framework.response   import Response
from rest_framework.request    import Request
from rest_framework.decorators import APIView

from routine.Model.Account       import Account
from routine.Model.Message       import Message
from routine.Model.Category      import Category
from routine.Model.Routine       import Routine
from routine.Model.RoutineDay    import RoutineDay
from routine.Model.RoutineResult import RoutineResult
from routine.Serializer.Message  import MessageSerializer
from routine.Functions.ClearData import isClearRoutineCreateData, isClearRoutineDeleteData

# /api/routine
class RoutineView(APIView):
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
        # data:    Final = request.data
        # jwt_str: Final = request.META.get('HTTP_TOKEN')

        # # 데이터 검증
        # if not isClearRoutineDeleteData(data, jwt_str):
        #     return Response( MessageSerializer( Message.getByCode( "ROUTINE_CREATE_FAIL" ) ).data, status=400 )
        
        # # header에 있는 JWT 꺼내기
        # email     = jwt.decode(jwt_str, SECRET_KEY)["email"]
        # account   = Account.objects.get( email = email )

        # # 로그인 상태인지 확인
        # if account.is_login == 0:
        #     return Response( MessageSerializer( Message.getByCode( "ROUTINE_CREATE_FAIL" ) ).data, status=400 )
        
        # # body data 꺼내기
        # routine_id = data["routine_id"]

        # routine         = Routine.objects.get(routine_id = routine_id)
        # routine_day     = RoutineDay.objects.get(routine_id = routine_id)
        # routine_results = RoutineResult.objects.filter( routine_id = routine_id )

        print(datetime.now())

        return Response("get")

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
            account_id = account.account_id, category_id = cateModel.category_id, title = title,
            is_alarm = 1 if is_alarm else 0, is_deleted = 0
        )

        # for day in days:
        #     RoutineDay.objects.create(
        #         routine_id = routine.routine_id, day = day
        #     )
        # RoutineDay.objects.bulk_create(
        #     [ RoutineDay( routine_id = routine.routine_id, day = day ) for day in days ]
        # )
        # RoutineDay.objects.create(
        #     routine_id = routine.routine_id, day = "|".join(days)
        # )

        RoutineResult.objects.create(
            routine_id = routine.routine_id, result_id = 1, is_deleted = 0
        )

        return Response({
            "data":    { "routine_id": routine.routine_id },
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

        Routine.objects.get(routine_id = routine_id).delete()
        RoutineDay.objects.get(routine_id = routine_id).delete()
        RoutineResult.objects.filter( routine_id = routine_id ).delete()

        return Response({
            "data":    { "routine_id": routine_id },
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