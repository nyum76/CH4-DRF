from rest_framework import serializers
from .models import Product, Comment

# 게시글 목록 조회 Serializer
class ProductListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email') # user 필드에 유저의 이메일만 출력
    
    class Meta:
        model = Product
        fields = ('id','user', 'title', 'created_at', 'view_count') # 조회수 필드 추가
        read_only_fields = ('user', ) # 외래키라 생성할 때 문제가 안 생김

# 게시글 상세 조회 및 생성 Serializer
class ProductDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email') # user 필드에 유저의 이메일만 출력
    
    class Meta:
        model = Product
        fields = ('id', 'user', 'title', 'content', 'created_at', 'updated_at', 'view_count') # 조회수 필드 추가


# 댓글 조회 및 생성 serializers
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField() # 좋아요 여부 - 가상 필드
    
    class Meta:
        model = Comment
        fields = ('id','product','user', 'content','created_at','updated_at','like_users','like_count','is_liked')
        read_only_fields = ('product', 'like_users') # 댓글 생성시 필요 없는 fields 명시
        
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(pk=request.user.pk).exists() # 현재 좋아요를 한 사람이 목록에 있는지 exists() 로 확인 -> 맞다면 True
        return False