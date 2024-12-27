from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .models import Product, Comment
from .serializers import ProductListSerializer, ProductDetailSerializer, CommentSerializer
from django.core.cache import cache


class ProductListCreate(APIView):
    # 권한 명시 : settings.py REST_FRAMEWORK
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):  # 상품 목록 조회
        # 1. 데이터 가져오기
        products = Product.objects.all()

        # 2. 직렬화
        serializer = ProductListSerializer(products, many=True)

        # 3. 데이터 돌려주기
        return Response(serializer.data)

    def post(self, request):  # 상품 등록
        serializer = ProductDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True): # 유효성 검사
            serializer.save(user=request.user) # permission 을 readonly 로 했기에 인자 넣어주기
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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


class CommentListCreate(APIView):
    '''댓글 CRUD'''
    def get_product(self, productId):
        return get_object_or_404(Product, pk=productId)


    def get(self, request, productId):
        '''댓글 조회'''
        product = self.get_product(productId)
        comments = product.comments.all() # 역참조로 모든 댓글 가져오기
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, productId):
        '''댓글 생성'''
        product = self.get_product(productId)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentLike(APIView):
    '''댓글 좋아요 기능'''
    def get_product(self, productId):
        return get_object_or_404(Product, pk=productId)
    
    def get_comment(self, product, commentId):
        return get_object_or_404(Comment, pk=commentId, product=product)

    def post(self, request, productId, commentId):
        product = self.get_product(productId)
        comment = self.get_comment(product, commentId)
        user = request.user
        
        # 이미 좋아요를 눌렀는지 확인
        if comment.like_users.filter(pk=user.pk).exists():
            # 좋아요 취소
            comment.like_users.remove(user)
            message = "댓글 좋아요가 취소되었습니다."
        else:
            # 좋아요 추가
            comment.like_users.add(user)
            message = "댓글을 좋아요 했습니다."

        # 댓글 정보를 serializer를 통해 반환
        serializer = CommentSerializer(comment, context={'request': request})
        
        return Response({
            'message': message,
            'comment': serializer.data
        }, status=status.HTTP_200_OK)