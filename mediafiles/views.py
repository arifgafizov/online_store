import os
from datetime import datetime, timedelta
from uuid import uuid4
import jwt

from rest_framework import views, status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

from mediafiles.media_constants import ACCEPTABLE_VALUES
from mediafiles.serializers import JWTTokenSerializer


class FileUploadView(views.APIView):
    # TODO декодировать токен и время его жизни
    # TODO Проверить расширение файла и домена из payload на соответствие domain аргументу пост запроса и file_extension
    # TODO сравнить размер файла на размер на который получил разрешение с отправленым или вернуть 403 error
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def post(self, request, domain):
        #  getting jwt token from headers Authorization
        jwt_token = request.headers.get('Authorization')
        print("jwt_token")
        print(jwt_token)
        # decoding jwt token
        with open('/home/arif/PycharmProjects/online_store/keys_jwt/jwtRS256.key.pub', 'r') as key:
            public_key = key.read()
        decoded = jwt.decode(jwt_token, public_key, algorithms=["RS256"])
        print('decoded')
        print(decoded)

        if decoded['domain'] != domain:
            return Response(data={'reason': "Invalid domain."}, status=status.HTTP_403_FORBIDDEN)

        def save_file(path, f):
            with open(path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        up_file = request.data['file']
        now = datetime.now()
        media_dir = os.path.join(settings.MEDIA_ROOT, domain, now.strftime("%Y%m%d"))
        os.makedirs(media_dir, exist_ok=True)
        file_extension = str(up_file).split('.')[-1]
        if decoded['extension'] != file_extension:
            return Response(data={'reason': "Invalid file extension."}, status=status.HTTP_403_FORBIDDEN)
        print(decoded['exp'])
        print(now.timestamp())
        print(decoded['exp'] <= now.timestamp())
        if decoded['exp'] > now.timestamp():
            return Response(data={'reason': "The jwt token expired."}, status=status.HTTP_403_FORBIDDEN)
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

        # getting data from the client
        domain = serializer.data['domain']
        extension = serializer.data['extension']
        file_size = serializer.data['file_size']

        JWT_ALGORITHM = 'RS256'
        JWT_EXP_DELTA_SECONDS = 60
        with open('/home/arif/PycharmProjects/online_store/keys_jwt/jwtRS256.key', 'r') as key:
            private_key = key.read()
        #TODO загрузить файл . Получение от клиента - Домен, расширение, размер файла
        # проверить данные от клиента на соответствие домена и расширения и проверка на размер файла. и положить их в тело jwt tokena
        # добавить время жизни токена в 1 минуту
        user_id = None if self.request.user.is_anonymous else self.request.user.id

        # checking for compliance of the domain and extension and for the file size
        if extension not in ACCEPTABLE_VALUES[domain]['extension']:
            raise ValidationError({"error": "The domain does not match the file extension."})
        if file_size > ACCEPTABLE_VALUES[domain]['size']:
            raise ValidationError({"error": "Invalid file size."})

        payload = {
            'user_id': user_id,
            'domain': domain,
            'extension': extension,
            'file_size': file_size,
            'exp': (datetime.now() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)).timestamp()
            }
        # generating jwt token with payload
        jwt_token = jwt.encode(payload, private_key, JWT_ALGORITHM, headers={"alg": "RS256", "typ": "JWT"})

        return Response({'token': jwt_token}, status=status.HTTP_201_CREATED)
