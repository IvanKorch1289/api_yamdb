from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from rest_framework import viewsets, filters, status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny)
from rest_framework.response import Response

from api.filters import TitleFilterSet
from api.permissions import (IsAdmin, ReadOnly,
                             IsAuthorOrModeratorOrReadOnly)
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitleGetSerializer,
                             ReviewSerializer, CommentSerializer,
                             UserSerializer, SignupSerializer, AdminSerializer)
from reviews.models import (Category, Genre,
                            Review, Title)

User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

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
    search_fields = ('name',)
    permission_classes = (IsAdmin,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed('GET')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    filterset_class = TitleFilterSet
    filter_fields = ('genre__slug',)
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
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete',]

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        if bool(self.request.user.is_authenticated
                and self.request.user.role == 'admin'):
            return (IsAdmin(),)
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        if Review.objects.filter(
            author=self.request.user
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def get_title(self):
        title_id = self.kwargs.get('title_id', None)
        title = get_object_or_404(
            Title,
            pk=title_id
        )
        return title

    def get_score(self):
        score = Review.objects.values_list(
            'score',
            flat=True
        )
        print(score)
        return score

    def save_rating(self, score):
        if score is not None:
            rating = sum(score) / len(score)
        else:
            rating = 0
        title = self.get_title()
        title.rating = rating
        title.save()

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        score = self.get_score()
        score = list(score).append(serializer.validated_data['score'])
        print(serializer.validated_data)
        self.save_rating(score)
        serializer.save(
            title=self.get_title(),
            author=self.request.user)

    def perform_update(self, serializer):
        last_score = self.get_score().get(
            pk=self.kwargs.get('pk', None))
        score = list(self.get_score())
        score.remove(last_score)
        score.append(serializer.validated_data['score'])
        self.save_rating(score)
        serializer.save()

    def perform_destroy(self, instance):
        last_score = self.get_score().get(
            pk=self.kwargs.get('pk', None))
        score = list(self.get_score())
        score.remove(last_score)
        self.save_rating(score)
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete',]

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        if bool(self.request.user.is_authenticated
                and self.request.user.role == 'admin'):
            return (IsAdmin(),)
        return super().get_permissions()

    def get_review(self):
        review_id = self.kwargs.get('review_id', None)
        review = get_object_or_404(
            Review,
            pk=review_id
        )
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            review=review,
            author=self.request.user
        )


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


class SignupViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ('post')

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_mail(
                subject='Код подтверждения',
                message=f'Ваш код: {user.confirmation_code}',
                from_email='info@api_yamdb.not',
                recipient_list=[user.email]
            )
            return Response(
                {'email': user.email, 'username': user.username},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
