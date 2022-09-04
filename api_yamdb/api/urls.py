from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, SignUpAPIView, TitlesViewSet, TokenAPIView,
                    UserViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='titlereviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='reviewcomments'
)
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpAPIView.as_view()),
    path('v1/auth/token/', TokenAPIView.as_view()),
]
