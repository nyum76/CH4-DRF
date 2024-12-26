from django.shortcuts import render
from rest_framework.decorators import api_view # DRF 에서는 api_view 없으면 동작 안 함
from .serializers import SignupSerializer
from rest_framework.response import Response
from rest_framework import status

@api_view(["POST"])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message":"회원가입이 성공적으로 완료되었습니다."
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)