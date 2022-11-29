from datetime import date
from rest_framework import serializers
from reviews.models import User, Comment, Review, Category, Genre, Title
from .utils import get_count_rating


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода информации о пользователе."""

    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        model = User


class EmailSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор для регистрации новых пользователей."""

    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('email', 'username',)
        model = User

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        return data

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError(
                'Данный адрес электронной почты занят, '
                'используйте другой адрес'
            )
        return data


class ConfirmationCodeSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанра."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleBaseSerializer(serializers.ModelSerializer):
    """Сериализатор для произведения."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField(method_name='_get_rating')

    class Meta:
        fields = '__all__'
        model = Title

    def _get_rating(self, obj):
        return get_count_rating(self, obj)


class TitleAddSerializer(TitleBaseSerializer):
    """Сериализатор для произведения."""

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError(
                'Нельзя добавить произведение из будущего.')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для обзора."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if Review.objects.filter(
                title_id=(
                    self.context['request'].
                    parser_context['kwargs']['title_id']
                ),
                author_id=self.context['request'].user).exists():
            raise serializers.ValidationError(
                {'error': 'Нельзя оставить много обзоров на одну запись'})
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментария."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        model = Comment
