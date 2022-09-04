import datetime as dt

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import (USER, Categories, Comments, Genres, GenresTitles,
                            Review, Title, User)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации новых пользователецй."""
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('email', 'username')
        model = User

    def validate(self, data):
        """Проверяем, что нельзя создать пользователя
         с существующим email и именем "me".
         """
        username = data['username']
        email = data['email']
        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя создать пользователя с username = "me"'
            )
        if User.objects.filter(email=email):
            raise serializers.ValidationError(
                'Нельзя создать пользователя,'
                'email которого уже зарегистрирован'
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    """Сериалайзер для JWT-токенов."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User

    def validate(self, data):
        """Проверяем, что нельзя создать пользователя "me"."""
        username = data['username']
        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать пользователя с username = "me"'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для Users."""
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        model = User

    def validate_role(self, data):
        """Пользователь с ролью "user" не должен мочь менять свою роль"""
        if self.context['request'].user.role == USER:
            data = USER
            return data
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для обзоров."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            title = int(request.parser_context.get('kwargs').get('title_id'))
            get_object_or_404(Title, pk=title)
            if Review.objects.filter(title_id=title).filter(
                    author_id=request.user.id).exists():
                raise serializers.ValidationError(
                    'Нельзя оставлять больше 1 отзыва')
            return data
        return data

    def validate_score(self, value):
        if value not in range(1, 11):
            raise serializers.ValidationError(
                'Оценка не в диапазоне от 1 до 10'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев на обзоры."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments

    def validate(self, data):
        request = self.context.get('request')
        review_id = int(request.parser_context.get('kwargs').get('review_id'))
        review = get_object_or_404(Review, pk=review_id)
        title_id = int(request.parser_context.get('kwargs').get('title_id'))
        title_check = get_object_or_404(Title, pk=title_id)
        if review.title != title_check:
            raise serializers.ValidationError(
                'Неправильное произведение'
            )
        return data


class CategorieSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений."""

    class Meta:
        fields = ('name', 'slug')
        model = Categories
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров произведений."""

    class Meta:
        fields = ('name', 'slug')
        model = Genres
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['view'].action in ('create', 'partial_update'):
            self.fields.update({
                "category": SlugRelatedField(
                    slug_field='slug',
                    queryset=Categories.objects.all()
                ),
                "genre": SlugRelatedField(
                    slug_field='slug',
                    queryset=Genres.objects.all(),
                    many=True),
            })

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorieSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category',
        )
        model = Title

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if rating:
            return round(rating, 1)

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            GenresTitles.objects.create(title=title, genre=genre)
        return title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.'
            )
        return value
