
from typing import Final
import jwt

from api.settings import SECRET_KEY

from rest_framework.response   import Response
from rest_framework.request    import Request
from rest_framework.decorators import APIView

from routine.Model.Account       import Account
from routine.Model.Message       import Message
from routine.Model.Category      import Category
from routine.Model.Routine       import Routine
from routine.Model.RoutineDay    import RoutineDay
from routine.Serializer.Message  import MessageSerializer
from routine.Functions.ClearData import isClearRoutineCreateData, isClearRoutineDeleteData

class RoutineView(APIView):
    # SEARCH
    def get(self, request: Request):
        pass

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

        routine_day = RoutineDay.objects.create(
            routine_id = routine.routine_id, day = "|".join(days)
        )

        return Response({
            "data":    { "routine_id": routine.routine_id },
            "message": MessageSerializer(Message.getByCode( "ROUTINE_CREATE_OK" )).data
        })

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

        Routine.objects.get(routine_id=routine_id).delete()
        RoutineDay.objects.get(routine_id=routine_id).delete()

        return Response({
            "data":    { "routine_id": routine_id },
            "message": MessageSerializer(Message.getByCode( "ROUTINE_DELETE_OK" )).data
        })

    # Update
    def put(self, request: Request):
        return Response("put")