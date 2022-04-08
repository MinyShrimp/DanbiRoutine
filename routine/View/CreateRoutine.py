
from typing import Final

import jwt

from api.settings import SECRET_KEY

from rest_framework.response   import Response
from rest_framework.request    import Request
from rest_framework.decorators import api_view

from routine.Model.Account       import Account
from routine.Model.Message       import Message
from routine.Model.Category      import Category
from routine.Model.Routine       import Routine
from routine.Model.RoutineDay    import RoutineDay
from routine.Model.RoutineResult import RoutineResult
from routine.Serializer.Message  import MessageSerializer
from routine.Serializer.Routine  import RoutineSerializer
from routine.Functions.ClearData import isClearRoutineCreateData
from routine.Token.EmailToken    import EmailToken

"""
루틴 생성
Request
{
    "title" : "",
    "category" : "HOMEWORK",
    "goal": "",
    "is_alarm": true,
    "days": ["MON", "WED", "FRI"]
}

Response
{
    "data": {
        "routine_id": 1
    },
    "message": {
        "msg": " .", "status": "ROUTINE_CREATE_OK"
    }
}
"""

@api_view(['POST'])
def CreateRoutine(request: Request):
    data:    Final = request.data
    jwt_str: Final = request.META.get('HTTP_TOKEN')

    # 데이터 검증
    if not isClearRoutineCreateData(data, jwt_str):
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_CREATE_FAIL" ) ).data, status=400 )

    title, category, goal, is_alarm, days = data["title"], data["category"], data["goal"], data["is_alarm"], data["days"]
    
    email     = jwt.decode(jwt_str, SECRET_KEY)["email"]
    account   = Account.objects.get( email = email )
    cateModel = Category.objects.get( title = category )

    if account.is_login == 0:
        return Response( MessageSerializer( Message.getByCode( "ROUTINE_CREATE_FAIL" ) ).data, status=400 )

    routine = Routine.objects.create( 
        account_id = account.account_id, category_id = cateModel.category_id, title = title,
        is_alarm = 1 if is_alarm else 0, is_deleted = 0
    )

    routine_day = RoutineDay.objects.create(
        routine_id = routine.routine_id, day = "|".join(days)
    )

    # routine_result = RoutineResult.objects.create(
    #     routine_id = routine.routine_id, is_deleted = 0, result_id  = 0
    # )

    return Response({
        "data":    { "routine_id": routine.routine_id },
        "message": MessageSerializer(Message.getByCode( "ROUTINE_CREATE_OK" )).data
    })