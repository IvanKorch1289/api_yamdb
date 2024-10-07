
from api.filters import TitleFilterSet
from api.permissions import IsAdmin, IsAuthorOrModeratorOrReadOnly, ReadOnly
from api.serializers import (AdminSerializer, CategorySerializer,
                             CommentSerializer, GenreSerializer,
                             ReviewSerializer, SignupSerializer,
                             TitleGetSerializer, TitleSerializer,
                             TokenSerializer, UserSerializer)
from api.utils import get_user_and_send_mail
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    permission_classes = (IsAdmin,)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        if bool(self.request.user.is_authenticated
                and self.request.user.role == 'admin'):
            return (IsAdmin(),)
        return super().get_permissions()

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id', None))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def create(self, request, *args, **kwargs):
        self.get_title()
        if Review.objects.filter(
            author=self.request.user
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        if bool(self.request.user.is_authenticated
                and self.request.user.role == 'admin'):
            return (IsAdmin(),)
        return super().get_permissions()

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id', None)
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(review=review, author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели User."""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin,)
    serializer_class = AdminSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        url_path='me',
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,)
    )
    def profile_update(self, request):
        serializer = UserSerializer(self.request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    user = User.objects.filter(username=request.data.get('username'))
    if user.exists() and request.data.get('email') == user[0].email:
        get_user_and_send_mail(user)
        return Response(request.data, status=status.HTTP_200_OK)

    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = User.objects.filter(**serializer.data)
        get_user_and_send_mail(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(request.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    request_code = serializer.validated_data['confirmation_code']
    if request_code == user.confirmation_code:
        token = RefreshToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
