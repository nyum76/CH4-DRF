from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'), # 로그인 url path
    path('logout/', views.logout, name='logout'), # 로그아웃 url path
    path('profile/', views.profile, name='profile'), # 회원정보 조회 및 수정
]
