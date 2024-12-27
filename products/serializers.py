from rest_framework import serializers
from .models import Article

# 게시글 목록 조회 Serializer
class ProductListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') # user 필드에 유저의 이메일만 출력
    
    class Meta:
        model = Article
        fields = ('id','user', 'title', 'created_at')

# 게시글 상세 조회 및 생성 Serializer
class ProductDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') # user 필드에 유저의 이메일만 출력
    
    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'content', 'created_at', 'updated_at',)