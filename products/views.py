from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer


class ProductListCreate(APIView):
    # 권한 명시 : settings.py REST_FRAMEWORK
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):  # 상품 목록 조회
        # 1. 데이터 가져오기
        products = Product.objects.all()

        # 2. 직렬화
        serializer = ProductListSerializer(products, many=True)

        # 3. 데이터 돌려주기
        return Response(serializer.data)

    def post(self, request):  # 상품 등록
        serializer = ProductDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True): # 유효성 검사
            serializer.save(user=request.user) # permission 을 readonly 로 했기에 인자 넣어주기
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):

    # 일관되게 처리할 수 있도록 메서드 설정 (유효성 검증 로직 등에서,,,)
    # 개발 패턴중 하나임 ! -- > 확장성, 보완성, 유지 보수성 .. 등이 좋기에 사용함 (getter ?)
    def get_object(self, articleId):
        # pk 값이 없을 시 404 error 출력
        return get_object_or_404(Product, pk=articleId)

    def get(self, request, articleId): # 상품 상세 조회
        # 1. product pk 조회
        product = self.get_object(articleId)
        # 2. 직렬화
        serializer = ProductDetailSerializer(product)
        # 3. 반환
        return Response(serializer.data)

    def put(self, request, articleId):
        product = self.get_object(articleId)
        serializer = ProductDetailSerializer(
            product,
            data=request.data,
            partial=True, # 부분적 수정 허용
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def delete(self, request, articleId):
        product = self.get_object(articleId)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
