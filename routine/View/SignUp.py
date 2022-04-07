from typing import Final
from rest_framework.response import Response
from rest_framework.request  import Request
from rest_framework.decorators import api_view
# from .models      import Account
# from .serializers import AccountSerializer

# Create your views here.
@api_view(['POST'])
def SignUp(request: Request):
    data: Final = request.data
    
    # account    = Account.objects.all()
    # serializer = AccountSerializer(account)
    return Response("hi")