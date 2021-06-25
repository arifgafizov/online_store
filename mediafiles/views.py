from django.shortcuts import render
from rest_framework import views, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=status.HTTP_200_OK)