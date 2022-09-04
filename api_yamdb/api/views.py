import uuid

from core.filters import TitlesFilter
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Categories, Genres, Review, Title, User

from .permissions import (AdminEdit, AdminOnly,
                          AuthorOrModearatorOrAdminChangePermission)
from .serializer import (CategorieSerializer, CommentSerializer,
                         GenreSerializer, ReviewSerializer,
                         SignUpSerializer, TitleSerializer,
                         TokenSerializer, UserSerializer)
from api_yamdb.settings import STAFF_EMAIL


class SignUpAPIView(APIView):
    """Регистрация и выдача confirmation_code"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        confirmation_code = uuid.uuid4()
        if serializer.is_valid():
            email = self.request.data['email']
            send_mail(
                'confirmation_code',
                f'Your confirmation_code: {confirmation_code}.',
                STAFF_EMAIL,
                [email],
                fail_silently=False,
            )
            serializer.save(confirmation_code=confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenAPIView(APIView):
    """Выдача JWT на основании confirmation_code"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=self.request.data['username']
        )
        confirmation_code = self.request.data['confirmation_code']
        if confirmation_code == user.confirmation_code:
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Работа с Users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (AdminOnly,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        """Метод для обработки запросов к me/."""
        user = get_object_or_404(User, username=self.request.user)
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review"""

    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AuthorOrModearatorOrAdminChangePermission,)

    def _get_title_id(self):
        return self.kwargs.get("title_id")

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self._get_title_id())
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self._get_title_id())
        serializer.save(
            title=title,
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment"""

    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AuthorOrModearatorOrAdminChangePermission,)

    def _get_review_id(self):
        return self.kwargs.get("review_id")

    def _get_title_id(self):
        return self.kwargs.get("title_id")

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self._get_review_id(),
                                   title=self._get_title_id())
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self._get_review_id(),
                                   title_id=self._get_title_id())
        serializer.save(
            review=review,
            author=self.request.user
        )


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Вьюсет для создания, получения и удаления"""
    permission_classes = (AdminEdit,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoriesViewSet(CreateListDestroyViewSet):
    """Вьюсет для категорий произведений."""
    queryset = Categories.objects.all()
    serializer_class = CategorieSerializer


class GenresViewSet(CreateListDestroyViewSet):
    """Вьюсет для жанров произведений."""
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для названий произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminEdit,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
