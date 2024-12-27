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
    username = models.CharField('닉네임', max_length=150)  # unique=True 제거
    profile_image = models.ImageField('프로필 이미지', upload_to='profile_images/', blank=True, null=True)
    
    # ManyToManyField로 팔로우 기능 구현
    following = models.ManyToManyField(
        'self',  # 자기 자신과의 관계
        symmetrical=False,  # 대칭 관계가 아님 (단방향)
        related_name='followers',  # 역참조 이름
        through='Follow',  # 중간 테이블
        blank=True, # seeding 할때 null 값이 포함되므로 지정해주기 (트러블 슈팅)
    )
    
    USERNAME_FIELD = 'email'    # 로그인 시 이메일 사용
    REQUIRED_FIELDS = []        # email은 자동으로 필수

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name='followed_users', on_delete=models.CASCADE)  # 팔로우를 하는 사용자
    following = models.ForeignKey(
        User, related_name='following_users', on_delete=models.CASCADE)  # 팔로우받는 사용자
    created_at = models.DateTimeField(auto_now_add=True)  # 팔로우한 시간

    class Meta:
        unique_together = ('follower', 'following')  # 중복 팔로우 방지
        
    def __str__(self):
        return f"{self.follower} follows {self.following}"