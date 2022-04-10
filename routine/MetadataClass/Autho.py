
from api.settings import SECRET_KEY

from rest_framework.response   import Response
from rest_framework.request    import Request
from rest_framework.decorators import APIView

from rest_framework.metadata   import BaseMetadata

class Autho(BaseMetadata):
    def determine_metadata(self, request: Request, view: APIView):
        return Response({
            "hi"
        }, status=403)