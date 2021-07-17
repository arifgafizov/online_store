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
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def post(self, request, domain):
        #  getting jwt token from headers Authorization
        array_jwt_token = request.headers.get('Authorization').split(' ')
        if len(array_jwt_token) != 2:
            raise ValidationError({'reason': "Invalid JWT token."}, code=status.HTTP_403_FORBIDDEN)
        jwt_token = array_jwt_token[-1]

        # reading a public key into public_key variable and decoding jwt token
        public_key = settings.JWT_PUBLIC_KEY
        try:
            decoded = jwt.decode(jwt_token, public_key, algorithms=["RS256"], verify_exp=True)
        except jwt.ExpiredSignatureError:
            raise ValidationError({'reason': "JWT token expired."}, code=status.HTTP_401_UNAUTHORIZED)
        except:
            raise ValidationError({'reason': "Invalid JWT token."}, code=status.HTTP_403_FORBIDDEN)

        up_file = request.data['file']
        now = datetime.now()
        media_dir = os.path.join(settings.MEDIA_ROOT, domain, now.strftime("%Y%m%d"))
        os.makedirs(media_dir, exist_ok=True)
        file_extension = str(up_file).split('.')[-1]

        # checking for valid domain
        if decoded['domain'] != domain:
            return Response(data={'reason': "Invalid domain."}, status=status.HTTP_403_FORBIDDEN)

        # checking for valid extension
        if decoded['extension'] != file_extension:
            return Response(data={'reason': "Invalid file extension."}, status=status.HTTP_403_FORBIDDEN)

        # checking for valid file size
        if decoded['file_size'] != up_file.size:
            return Response(data={'reason': "Invalid file size."}, status=status.HTTP_403_FORBIDDEN)

        file_name = f'{int(now.timestamp())}_{uuid4()}.{file_extension}'
        path_to_file = os.path.join(media_dir, file_name)

        def save_file(path, f):
            with open(path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        save_file(path_to_file, up_file)

        upload_path = settings.MEDIA_URL + path_to_file.split('media/')[-1]

        return Response(data={'file': upload_path}, status=status.HTTP_201_CREATED)


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
        # reading a private key into private_key variable
        private_key = settings.JWT_PRIVATE_KEY
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
