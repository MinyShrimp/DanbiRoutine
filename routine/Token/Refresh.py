
from typing   import Final

from rest_framework.response         import Response
from rest_framework.request          import Request
from rest_framework.decorators       import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from routine.Log.Log                 import Log
from routine.Model.Message           import Message
from routine.Serializer.Message      import MessageSerializer

class Refresh(APIView):
    def post(self, request: Request):
        refresh_token: Final = request.data["refresh"]
        
        if refresh_token == "":
            Log.instance().error( "REFRESH: REFRESH_TOKEN_NULL" )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_JWT_REFRESH_FAIL" ) ).data, status=400)

        try:
            new_token = RefreshToken(refresh_token)
            return Response({ "access": str(new_token.access_token) })
        except Exception as e:
            Log.instance().error( "REFRESH: REFRESH_TOKEN_UNVAILED" )
            return Response( MessageSerializer( Message.getByCode( "ROUTINE_JWT_REFRESH_UNVAILED" ) ).data, status=400)