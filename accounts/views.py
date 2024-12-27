from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    SignupSerializer,
    UserUpdateSerializer,
    UserProfileSerializer,
)

from rest_framework.decorators import (
    api_view , # DRF 에서는 api_view 없으면 동작 안 함
    authentication_classes,
    permission_classes,
)

@api_view(["POST"])
@authentication_classes([]) # 전역 인증 설정 무시
@permission_classes([]) # 전역 IsAuthenticated 설정 무시
def signup(request):
    '''회원 가입'''
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
    '''로그인'''
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


@api_view(["POST"])
@authentication_classes([])      # 전역 인증 설정 무시
@permission_classes([])  # 전역 IsAuthenticated 설정 무시
def logout(request):
    '''로그아웃'''
    print('---')
    try:
        refresh_token = request.data.get("refresh")
        print(refresh_token)
        token = RefreshToken(refresh_token)
        print(token)
        token.blacklist()
        print('---')
        return Response({"message": "로그아웃 성공"})
    except Exception:
        return Response({"error": "로그아웃 실패"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'PATCH'])
def profile(request):

    user = request.user  # JWT 인증을 통해 얻은 현재 사용자
    
    if request.method == 'GET':
        '''프로필 조회'''
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data, status=200)
    
    if request.method in ('PUT', 'PATCH') :
        '''프로필 수정'''
        serializer = UserUpdateSerializer(instance=user, data=request.data, partial=True)  # partial=True로 일부 업데이트 허용

        if serializer.is_valid():
            serializer.save()  # 수정 내용 저장
            return Response({
                "message": "✨회원정보가 성공적으로 수정되었습니다",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def follow(request, user_pk):
    '''팔로우 기능'''
    profile_user = get_object_or_404(User, pk=user_pk)
    me = request.user

    if me == profile_user:
        return Response({'error': '자기 자신을 팔로우할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if me.following.filter(pk=profile_user.pk).exists():
        me.following.remove(profile_user)
        is_followed = False
        message = f'{profile_user.email}님 팔로우를 취소했습니다.'
    else:
        me.following.add(profile_user)
        is_followed = True
        message = f'{profile_user.email}님을 팔로우했습니다.'

    return Response({
        'is_followed': is_followed,
        'message': message,
    }, status=status.HTTP_200_OK)
