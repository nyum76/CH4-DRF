from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ProductListCreate.as_view(), name='article_list_create'), # 상품 등록, 조회
    path('<int:productId>/', views.ProductDetail.as_view(), name='article_detail'), # 상품 수정, 삭제
    path('<int:productId>/comments/', views.CommentListCreate.as_view(), name='comments'), # 댓글 조회, 생성
    path('<int:productId>/comments/<int:commentId>/like/', views.CommentLike.as_view(), name='comment_like'), # 댓글 좋아요 기능
]
