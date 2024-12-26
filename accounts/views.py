from django.shortcuts import render
from .serializers import SignupSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import (
    api_view , # DRF 에서는 api_view 없으면 동작 안 함
    authentication_classes,
    permission_classes,
)

@api_view(["POST"])
@authentication_classes([]) # 전역 인증 설정 무시
@permission_classes([]) # 전역 IsAuthenticated 설정 무시
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message":"회원가입이 성공적으로 완료되었습니다."
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 사용자 인증
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'access':str(refresh.access_token),
                'refresh':str(refresh),
                'message':'로그인 성공'
            },status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error':'이메일 또는 비밀번호가 올바르지 않습니다!!'}, status=400)


def logout(request):
    pass