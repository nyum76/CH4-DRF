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


## 기능
- 게시글 상세 조회 기능
![](/image/feat_product_detail.png)



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

## django_seed.exceptions.SeederException: Field accounts.User.following cannot be null
<details>
<summary><b>명령어와 해당 에러 코드</b></summary>
<div markdown="1">

```
❯ python3 manage.py seed products --number=20 --seeder "Product.user_id" 1
{'verbosity': 1, 'settings': None, 'pythonpath': None, 'traceback': False, 'no_color': False, 'force_color': False, 'skip_checks': False, 'number': 20, 'seeder': [['Product.user_id', '1']]}
Seeding 20 Users
Custom seeder {'user_id': '1'}
Seeding 20 Products
WARNING:root:Could not build many-to-many relationship for between accounts.User.groups and <class 'django.contrib.auth.models.Group'>
WARNING:root:Could not build many-to-many relationship for between accounts.User.user_permissions and <class 'django.contrib.auth.models.Permission'>
Traceback (most recent call last):
  File "/Users/t2023-m0072/Desktop/CH4-DRF/manage.py", line 22, in <module>
    main()
  File "/Users/t2023-m0072/Desktop/CH4-DRF/manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "/Users/t2023-m0072/Desktop/CH4-DRF/venv/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
    utility.execute()
  File "/Users/t2023-m0072/Desktop/CH4-DRF/venv/lib/python3.11/site-packages/django/core/management/__init__.py", line 436, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/Users/t2023-m0072/Desktop/CH4-DRF/venv/lib/python3.11/site-packages/django/core/management/base.py", line 412, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/Users/t2023-m0072/Desktop/CH4-DRF/venv/lib/python3.11/site-packages/django/core/management/base.py", line 458, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/t2023-m0072/Desktop/CH4-DRF/venv/lib/python3.11/site-packages/django/core/management/base.py", line 639, in handle
    app_output = self.handle_app_config(app_config, **options)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/t2023-m0072/Desktop/CH4-DRF/venv/lib/python3.11/site-packages/django_seed/management/commands/seed.py", line 63, in handle_app_config
    generated = seeder.execute()
                ^^^^^^^^^^^^^^^^
  File "/Users/t2023-m0072/Desktop/CH4-DRF/venv/lib/python3.11/site-packages/django_seed/seeder.py", line 250, in execute
    executed_entity = entity.execute(using, inserted_entities)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/t2023-m0072/Desktop/CH4-DRF/venv/lib/python3.11/site-packages/django_seed/seeder.py", line 172, in execute
    list = list(inserted_entities)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/t2023-m0072/Desktop/CH4-DRF/venv/lib/python3.11/site-packages/django_seed/seeder.py", line 62, in func
    raise SeederException(message)
django_seed.exceptions.SeederException: Field accounts.User.following cannot be null
```

</div>
</details>
![](/image/following_cannot_be_null_error.png)

에러 코드를 확인해보니 `accounts.User.following` 이라는 필드는 null 값을 허용하지 않는데, seeding 과정에서 null 값이 들어가서 에러가 발생한 것이다.

아래는 문제의 User 모델의 following 필드 코드이다.

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

문제를 해결하기 위해 빈 값이 허용이 안 됐던 following 을 빈 값을 허용하도록 바꿔준다.

![](/image/edited_user_model.png)

이후 다시 seeding 시도
```bash
python3 manage.py seed products --number=20 --seeder "Product.user_id" 1
```
![](/image/seeding_success.png)