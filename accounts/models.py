from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager # 계정관련 ORM 처리 class

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다!!')
        email = self.normalize_email(email) # 공백제거, 소문자로 변환
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    # 관리자 계정 생성 메서드
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField('이메일', unique=True)
    # username 안쓰려면 None 값 줘도 됨
    username = models.CharField('닉네임',max_length=150)
    # 프로필 이미지는 필수는 아니므로 빈값과 null 허용
    profile_image = models.ImageField('프로필 이미지', upload_to='profile_images/', blank=True, null=True)
    
    USERNAME_FIELD = 'email' # 로그인시 필요한 필드 (username 이 기본값이지만, email 로 로그인 하도록 명시)
    REQUIRED_FIELDS = [] # 필수 필드 정의 (email 필드는 자동으로 필수임)
    
    objects = CustomUserManager() # manager 를 내가 커스텀한 CustomUserManager 로 사용하겠다
    def __str__(self):
        return self.email