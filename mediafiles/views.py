import os
from datetime import datetime
from uuid import uuid4

from rest_framework import views, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings


class FileUploadView(views.APIView):
    # TODO добавить авторизацию по JWT токену
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def post(self, request, domain):

        def save_file(path, f):
            with open(path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        up_file = request.data['file']
        now = datetime.now()
        media_dir = os.path.join(settings.MEDIA_ROOT, domain, now.strftime("%Y%m%d"))
        os.makedirs(media_dir, exist_ok=True)
        file_extension = str(up_file).split('.')[-1]
        file_name = f'{int(now.timestamp())}_{uuid4()}.{file_extension}'
        path_to_file = os.path.join(media_dir, file_name)

        save_file(path_to_file, up_file)

        upload_path = settings.MEDIA_URL + path_to_file.split('media/')[-1]

        return Response(data={'file': upload_path}, status=status.HTTP_201_CREATED)


# TODO эндпоинт получение JWT токена