# CH4-DRF
챕터 4 DRF 를 활용한 스파르타 마켓 백엔드 기능 구현
- [ ] : `urls.py` path `api/accounts/` 으로 변경
- [ ] : 발제 노션 보고 요구사항에 맞게 코드 수정

## 초기 설정
- [x] : `.gitignore` 설정
- [X] : 가상환경 설정
```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate
```
- [X] : `spartamarket_DRF` 프로젝트 생성
```bash
django-admin startproject spartamarket_DRF .
```
- [X] : `accounts`, `products` 앱 생성
```bash
python3 manage.py startapp accounts
python3 manage.py startapp products
```

- 모델 새로 정의 할 때마다
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## AttributeError at /accounts/2/follow/
'User' object has no attribute 'followings'
![](/image/Attribute_error_follow.png)

User 모델에 following 이라고 지정해 놓고 `views.py` 에서 following**s** 로 일치 시키지 않아 발생함

* `models.py`
```py
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
    )
    
    USERNAME_FIELD = 'email'    # 로그인 시 이메일 사용
    REQUIRED_FIELDS = []        # email은 자동으로 필수

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
```

* `views.py`
```py
@api_view(["POST"])
def follow(request, user_pk):
    profile_user = get_object_or_404(User, pk=user_pk)
    me = request.user

    if me == profile_user:
        return Response({'error': '자기 자신을 팔로우할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if me.followings.filter(pk=profile_user.pk).exists():
        me.followings.remove(profile_user)
        is_followed = False
        message = f'{profile_user.email}님 팔로우를 취소했습니다.'
    else:
        me.followings.add(profile_user)
        is_followed = True
        message = f'{profile_user.email}님을 팔로우했습니다.'

    return Response({
        'is_followed': is_followed,
        'message': message,
    }, status=status.HTTP_200_OK)
```

![](/image/followers_to_following.png)

followings 이라고 적힌 모든 코드를 following 로 변경하니 성공

![](/image/following_success.png)