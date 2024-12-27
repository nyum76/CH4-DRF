from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ProductListCreate.as_view(), name='article_list_create'), # 상품 등록, 조회
    path('<int:articleId>/', views.ProductDetail.as_view(), name='article_detail'), # 상품 수정, 삭제
]
