from django.db import models
from django.conf import settings

# 원래 model 은 ERD 를 먼저 만들고 이를 바탕으로 구현
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products') # FK1
    title = models.CharField('제목', max_length=200)
    content = models.TextField('내용')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField('조회수', default=0) # 조회수 필드 추가
    
    def __str__(self):
        return self.title
# model 하나 만들어줄 때마다 makemigrations, migrate 진행


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments') # FK1
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # FK2
    content = models.TextField('내용')
    created_at = models.DateTimeField('작성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments') # 댓글 좋아요 기능 - m:n
    
    def __str__(self):
        return f'{self.user} - {self.content}'