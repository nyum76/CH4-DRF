from rest_framework import serializers
from .models import Product

# 게시글 목록 조회 Serializer
class ProductListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email') # user 필드에 유저의 이메일만 출력
    
    class Meta:
        model = Product
        fields = ('id','user', 'title', 'created_at', 'view_count') # 조회수 필드 추가
        read_only_fields = ('user', )

# 게시글 상세 조회 및 생성 Serializer
class ProductDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email') # user 필드에 유저의 이메일만 출력
    
    class Meta:
        model = Product
        fields = ('id', 'user', 'title', 'content', 'created_at', 'updated_at', 'view_count') # 조회수 필드 추가