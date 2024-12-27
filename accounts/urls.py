from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.signup, name='signup'), # 회원가입
    path('login/', views.login, name='login'), # 로그인
    path('logout/', views.logout, name='logout'), # 로그아웃 (도전 구현)
    path('profile/', views.profile, name='profile'), # 회원정보 조회 및 수정 (도전 구현)
    path('<int:user_pk>/follow/', views.follow, name='follow'), # follow 기능
]