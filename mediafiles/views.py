import os
from datetime import datetime, timedelta
from uuid import uuid4
import jwt

from rest_framework import views, status, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

from mediafiles.serializers import JWTTokenSerializer


class FileUploadView(views.APIView):
    # TODO декодировать токен и время его жизни
    # TODO Проверить расширение файла и домена из payload на соответствие domain аргументу пост запроса и file_extension
    # TODO сравнить размер файла на размер на который получил разрешение с отправленым или вернуть 403 error
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


# TODO эндпоинт получение JWT токена ассиметричные. Сгенирировать пару открытый и закрытый ключ по алгоритму RS256
class JWTTokenView(generics.GenericAPIView):
    serializer_class = JWTTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        domain = serializer.data['domain']
        extension = serializer.data['extension']
        file_size = serializer.data['file_size']
        print(domain, extension, file_size, type(file_size))

        JWT_ALGORITHM = 'RS256'
        JWT_EXP_DELTA_SECONDS = 60
        with open('/home/arif/PycharmProjects/online_store/keys_jwt/jwtRS256.key', 'r') as key:
            private_key = key.read()
        #TODO загрузить файл . Получение от клиента - Домен, расширение, размер файла
        # проверить данные от клиента на соответствие домена и расширения и проверка на размер файла. и положить их в тело jwt tokena
        # добавить время жизни токена в 1 минуту
        user_id = None if self.request.user.is_anonymous else self.request.user.id
        payload = {
            'user_id': user_id,
            'exp': (datetime.now() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)).timestamp()
        }

        jwt_token = jwt.encode(payload, private_key, JWT_ALGORITHM, headers={"alg": "RS256", "typ": "JWT"})

        # проверка декодировки
        # with open('/home/arif/PycharmProjects/online_store/keys_jwt/jwtRS256.key.pub', 'r') as key:
        #     public_key = key.read()
        # decoded = jwt.decode(jwt_token, public_key, algorithms=["RS256"])
        # print('decoded')
        # print(decoded)

        return Response({'token': jwt_token}, status=status.HTTP_201_CREATED)
