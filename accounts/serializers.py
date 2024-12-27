# Django 의 form 역할을 serializers 가 한다.
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# User 모델은 전역 변수로 설정
User = get_user_model()

# 회원가입용 Serializer
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True) # 비밀번호 확인용이라 validator 는 없음
    
    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'username', 'profile_image')
        
    # 내장되어있는 validate 실행 후 각 field 마다 validator 가 지정되어있을 경우 알아서 검증해 줌.
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                "password":"비밀번호가 일치하지 않습니다."
            })
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2') # password2 제거
        return User.objects.create_user(**validated_data)
    
    #accounts/serializers.py

class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    class FollowSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['email', 'username', 'profile_image']  # 반환할 필드

    followers = FollowSerializer(many=True, read_only=True)
    followings = FollowSerializer(many=True, read_only=True)
    follower_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)
    profile_image = serializers.SerializerMethodField() # 커스텀 필드로 처리
    
    class Meta:
        model = User
        fields = ['email','username','profile_image','followings','followers','follower_count','following_count'] # 반환할 필드
    
    
    def get_profile_image(self, obj):
        request = self.context.get('request')  # Serializer context에서 request 가져오기
        if obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url)
        return None


# 회원 정보 수정용 serializer
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'profile_image')  # 수정 가능한 필드