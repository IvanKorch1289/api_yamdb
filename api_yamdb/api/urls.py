from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoriesViewSet, GenresViewSet,
                       TitlesViewSet, ReviewsViewSet,
                       CommentsViewSet, UserViewSet)


router = DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)
router.register(
    r'titles\/(?P<title_id>\d+)\/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router.register(
    r'titles\/(?P<title_id>\d+)\/reviews\/(?P<review_id>\d+)\/comments',
    CommentsViewSet,
    basename='comments'
)
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('auth/signup', include('djoser.urls.jwt')),
]
