import os
from datetime import datetime

from rest_framework import views, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings


class FileUploadView(views.APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]


    def post(self, request, domain):

        def save_file(path, f):
            with open(path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        up_file = request.data['file']
        now = datetime.now().isoformat()
        media_dir = os.path.join(settings.MEDIA_ROOT, domain, now)
        os.makedirs(media_dir, exist_ok=True)
        path_to_file = os.path.join(media_dir, str(up_file))

        save_file(path_to_file, up_file)

        return Response(status.HTTP_201_CREATED)
