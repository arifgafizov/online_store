import os

from rest_framework import views, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings


class FileUploadView(views.APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]


    def post(self, request, domain, format='jpg'):
        def save_file(path, f):
            with open(path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        up_file = request.data['file']
        dir = os.path.join(settings.MEDIA_ROOT, domain)
        os.makedirs(dir, exist_ok=True)
        path = os.path.join(dir, str(up_file))

        save_file(path, up_file)

        return Response(status.HTTP_201_CREATED)
