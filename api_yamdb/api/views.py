from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from rest_framework import viewsets, filters, status, permissions
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from review.models import (Categories, Comments, Genres,
                           Reviews, Titles)

from .permissions import (IsAuthorOrReadOnly, IsAdmin, IsModerator,
                          ReadOnly)
from api.serializers import (CategoriesSerializer, GenresSerializer,
                             TitlesSerializer, ReviewsSerializer,
                             CommentsSerializer, UserSerializer)

User = get_user_model()


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    # permission_classes = (IsAuthorOrReadOnly,)

    def create(self, request, *args, **kwargs):
        if Reviews.objects.filter(
            author=self.request.user
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def get_title(self):
        title_id = self.kwargs.get('title_id', None)
        title = get_object_or_404(
            Titles,
            pk=title_id
        )
        return title

    def get_score(self):
        score = Reviews.objects.values_list(
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
            pk=self.kwargs.get('review_id', None))
        score = self.get_score()
        score.pop(last_score)
        score.append(serializer.validated_data['score'])
        self.save_rating(score)
        serializer.save()

    def perform_destroy(self, instance):
        last_score = self.get_score().get(
            pk=self.kwargs.get('review_id', None))
        score = self.get_score()
        score.pop(last_score)
        self.save_rating(score)
        instance.delete()


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_review(self):
        review_id = self.kwargs.get('review_id', None)
        review = get_object_or_404(
            Reviews,
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
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=True, url_path='me/', methods=['get', 'patch'], permission_classes=(IsAuthenticated,))
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
