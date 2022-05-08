from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (viewsets, filters, permissions, filters,)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import (PageNumberPagination,
                                       LimitOffsetPagination)
from rest_framework.generics import CreateAPIView

from reviews.models import Category, Genre, Review, Title
from .permissions import (OwnerAdminModeratorOrReadOnly, TitlePermission,
                          IsOnlyAdmin, IsOwnerOrReadOnly,)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TokenSerializer, SignUpSerializer, UserSerializer,
                          TitleCreateSerializer)
from .utils import (create_code,
                    create_token,
                    message_sign_up,)
from .mixins import GenreCategoryMixin
from .filters import TitleFilter

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (TitlePermission,)
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')).order_by('name')
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateSerializer
        return TitleSerializer


class GenreViewSet(GenreCategoryMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (OwnerAdminModeratorOrReadOnly,)
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (OwnerAdminModeratorOrReadOnly,)
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return serializer.save(author=self.request.user, review=review)


class SignUpView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        name = serializer.validated_data['username']
        confirmation_code = create_code()
        serializer.save(confirmation_code=confirmation_code)
        message_sign_up(name, confirmation_code, email)
        return Response(serializer.data)


class TokenView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        response = create_token(user)
        return Response(response)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOnlyAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly],
    )
    def my_profile(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(self.request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(
            self.request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=self.request.user.role)
        return Response(serializer.data)
