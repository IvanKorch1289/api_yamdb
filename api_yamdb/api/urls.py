from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoriesViewSet, GenresViewSet,
                       TitlesViewSet, ReviewsViewSet,
                       CommentsViewSet)


router = DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenresViewSet)
router.register(r'titles', TitlesViewSet)
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


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),
]
