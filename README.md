## 📖 목차
- [📖 목차](#-목차)
- [🔥 스파르타 마켓](#-스파르타-마켓)
- [초기 설정](#초기-설정)
- [✨ 주요기능](#-주요기능)
  - [🧑‍💻 **회원 기능**](#-회원-기능)
  - [📋 **게시 기능**](#-게시-기능)
  - [💬 **댓글 기능**](#-댓글-기능)
- [📚️ 기술스택](#️-기술스택)
- [ERD](#erd)
- [프로젝트 파일 구조](#프로젝트-파일-구조)
- [Trouble Shooting](#trouble-shooting)
    - [AttributeError at /accounts/2/follow/](#attributeerror-at-accounts2follow)
      - [django\_seed.exceptions.SeederException: Field accounts.User.following cannot be null](#django_seedexceptionsseederexception-field-accountsuserfollowing-cannot-be-null)
    
## 🔥 스파르타 마켓
챕터 4
DRF (Django REST Framework) 를 활용한 스파르타 마켓 백엔드 구현

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


## ✨ 주요기능


### 🧑‍💻 **회원 기능**

<details>
<summary><b>회원가입</b></summary>
<div markdown="1">

`/api/accounts/` - `POST`
![](/image/signin_postman.png)

</div>
</details>


<details>
<summary><b>로그인</b></summary>
<div markdown="1">

`/api/accounts/login/` - POST

![](/image/login_postman.png)

</div>
</details>


<details>
<summary><b>로그아웃</b></summary>
<div markdown="1">

`/api/accounts/logout/` - `POST`

로그인 후 받은 `refresh` 값을 넣으면 로그아웃됨

![](/image/logout_postman.png)

</div>
</details>


<details>
<summary><b>프로필 조회</b></summary>
<div markdown="1">

`/api/accounts/profile/` - `GET`

로그인 후 받은 access token 을 auth - Bearer Token 에 넣으면 됨

![](/image/profile_get_postman.png)


```py
@api_view(['GET', 'PUT', 'PATCH'])
def profile(request):

    user = request.user  # JWT 인증을 통해 얻은 현재 사용자
    
    if request.method == 'GET':
        '''프로필 조회'''
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data, status=200)
    
    if request.method in ('PUT', 'PATCH') :
        '''프로필 수정'''
        serializer = UserUpdateSerializer(instance=user, data=request.data, partial=True)  # partial=True로 일부 업데이트 허용

        if serializer.is_valid():
            serializer.save()  # 수정 내용 저장
            return Response({
                "message": "✨회원정보가 성공적으로 수정되었습니다",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

</div>
</details>



<details>
<summary><b>회원 정보 수정</b></summary>
<div markdown="1">

프로필 조회와 마찬가지로,
로그인 후 받은 access token 을 auth - Bearer Token 에 넣은 후

username 이나 profile image 중 아무거나 수정 가능 (하나만 수정도 가능)

`/api/accounts/<str:username>/` - `PUT`

![](/image/profile_edit_postman.png)

```py
@api_view(['GET', 'PUT', 'PATCH'])
def profile(request):

    user = request.user  # JWT 인증을 통해 얻은 현재 사용자
    
    if request.method == 'GET':
        '''프로필 조회'''
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data, status=200)
    
    if request.method in ('PUT', 'PATCH') :
        '''프로필 수정'''
        serializer = UserUpdateSerializer(instance=user, data=request.data, partial=True)  # partial=True로 일부 업데이트 허용

        if serializer.is_valid():
            serializer.save()  # 수정 내용 저장
            return Response({
                "message": "✨회원정보가 성공적으로 수정되었습니다",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

</div>
</details>


<details>
<summary><b>팔로우/언팔로우</b></summary>
<div markdown="1">

`/api/accounts/<int:user_pk>/follow/` - `POST`

마찬가지로 access token 을 auth 에 넣고 `<int:user_pk>` 에 팔로우 할 유저의 pk 값을 넣어주면 팔로우됨.

다시 send 하면 언팔로우

![](/image/follow_postman.png)

</div>
</details>

---


### 📋 **게시 기능**

<details>
<summary><b>상품 등록</b></summary>
<div markdown="1">

`/api/products/` - `POST`

![](/image/product_created_postman.png)

</div>
</details>



<details>
<summary><b>상품 목록 조회</b></summary>
<div markdown="1">

`/api/products/` - `GET`

![](/image/product_list_postman.png)

</div>
</details>








<details>
<summary><b>상품 상세 조회 + 조회수 기능</b></summary>
<div markdown="1">

`/api/products/<int:productId>/` - `GET`


![](/image/product_detail_postman.png)

게시글 상세보기하면 조회수가 증가함

- 로그인한 사용자여야 하고, 작성자가 아닌 경우에만 조회수가 증가하도록 함
- 24 시간동안 같은 IP에서 같은 게시글 조회시 조회수 증가 X

```py
class ProductDetail(APIView):

    # 일관되게 처리할 수 있도록 메서드 설정 (유효성 검증 로직 등에서,,,)
    # 개발 패턴중 하나임 ! -- > 확장성, 보완성, 유지 보수성 .. 등이 좋기에 사용함 (getter ?)
    def get_object(self, productId):
        # pk 값이 없을 시 404 error 출력
        return get_object_or_404(Product, pk=productId)

    def get(self, request, productId):
        '''상품 상세 조회'''
        # 1. product pk 조회
        product = self.get_object(productId)
        
        # 수정한 조회수
        # 로그인한 사용자이고 작성자가 아닌 경우에만 조회수 증가 처리
        # 24시간 동안 같은 IP에서 같은 게시글 조회 시 조회수가 증가하지 않음
        if request.user != product.user:
            # 해당 사용자의 IP와 게시글 ID로 캐시 키를 생성
            cache_key = f"view_count_{request.META.get('REMOTE_ADDR')}_{productId}"
        
            # 캐시에 없는 경우에만 조회수 증가
            if not cache.get(cache_key):
                product.view_count += 1
                product.save()
                # 캐시 저장 (24시간 유효)
                cache.set(cache_key, True, 60*60*24)
        
        # 기존의 조회수
        # product.view_count += 1
        # product.save()
        
        # 2. 직렬화
        serializer = ProductDetailSerializer(product)
        # 3. 반환
        return Response(serializer.data)

    def put(self, request, productId):
        '''상품 수정'''
        product = self.get_object(productId)
        serializer = ProductDetailSerializer(
            product,
            data=request.data,
            partial=True, # 부분적 수정 허용
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, productId):
        '''상품 삭제'''
        product = self.get_object(productId)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

</div>
</details>

<details>
<summary><b>상품 수정</b></summary>
<div markdown="1">

`/api/products/<int:productId>/` - `PUT`

![](/image/product_edit_postman.png)

</div>
</details>



<details>
<summary><b>상품 삭제</b></summary>
<div markdown="1">

`/api/products/<int:productId>/` - `DELETE`

![](/image/product_delete_postman.png)

목록 조회해보면 1번글이 삭제된 모습

![](/image/product_deleted_postman.png)

</div>
</details>

---

### 💬 **댓글 기능**

<details>
<summary><b>댓글 생성</b></summary>
<div markdown="1">

`/api/products/<int:productId>/comments/` - `POST`

![](/image/create_comment_postman.png)

</div>
</details>

<details>
<summary><b>댓글 조회</b></summary>
<div markdown="1">

`/api/products/<int:productId>/comments/` - `GET`

![](/image/comment_get_postman.png)

</div>
</details>


<details>
<summary><b>댓글 좋아요 기능</b></summary>
<div markdown="1">

`/api/accounts/logout/` - `POST`

한 번 누르면 좋아요
![](/image/comment_like_postman.png)

한 번 더 누르면 좋아요 취소

![](/image/comment_unlike_postman.png)

</div>
</details>



## 📚️ 기술스택
<div align=center>
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=greene">
<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white">
<img src="https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white">
<img src="https://img.shields.io/badge/Sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">
<br>
<img src="https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white">
<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">

<img src="https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white">
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">



</div>


## ERD
![](/image/DRF-ERD.png)

## 프로젝트 파일 구조


```
spartamarket_DRF
├── README.md : README 문서
├── accounts/ : 계정 관련 기능 앱
├── products/ : 상품 관련 기능 앱
├── spartamarket_DRF/ : 프로젝트 앱
│
├── image/ : 자원 경로
├── media/ : 자원 경로
│
├── manage.py : 프로젝트 관리 수행 파일
├── requirements.txt : 프로젝트에 사용된 패키지 목록 파일
```
## Trouble Shooting


<details>
<summary><b>follow 시도중 안 됨</b></summary>
<div markdown="1">

#### AttributeError at /accounts/2/follow/
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

</div>
</details>


<details>
<summary><b>seed 생성 안 됨</b></summary>
<div markdown="1">

##### django_seed.exceptions.SeederException: Field accounts.User.following cannot be null

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

</div>
</details>