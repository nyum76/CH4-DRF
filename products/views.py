from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer

class ProductListCreate(APIView):
    
    def get(self, request): # 상품 목록 조회
        # 1. 데이터 가져오기
        products = Product.objects.all()
        
        # 2. 직렬화
        serializer = ProductListSerializer(
            products, many=True
        )
        
        # 3. 데이터 돌려주기
        return Response(serializer.data)

    def post(self, request): # 상품 등록
        serializer = ProductDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
