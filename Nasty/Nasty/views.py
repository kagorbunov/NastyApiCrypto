import base64
import json

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework.response import Response
from rest_framework import status

from .extractor import jopa

class PhotoBinaryViewSet(APIView):
    parser_classes = (MultiPartParser, JSONParser,)

    def post(self, request, *args, **kwargs):
        base64_img = request.data['file']
        base64_img_bytes = base64_img.encode('utf-8')
        with open("D:\\imageToSave.jpg",
                  "wb") as file_to_save:
            decoded_image_data = base64.decodebytes(base64_img_bytes)
            file_to_save.write(decoded_image_data)

        dig = jopa("D:\\imageToSave.jpg")
        answer = {
            "char" : str(dig)
        }
        return Response(answer, status=status.HTTP_200_OK)
