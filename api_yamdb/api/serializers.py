from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    def validate_year(self, value):
        year = timezone.now().year
        if value > year:
            raise serializers.ValidationError('Проверьте год выхода!')
        return value

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        exclude = ['title']
        model = Review
        read_only_fields = ['review']

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            title_id = int(self.context.get('view').kwargs['title_id'])
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(
                title=title,
                author=self.context.get('request').user
            ).exists():
                raise ValidationError(
                    'Данный пользователь уже оставлял отзыв о сабже'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        exclude = ['review']
        model = Comment
        read_only_fields = ['review']


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Username unavailable'
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=16)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = user.confirmation_code
        if data['confirmation_code'] != confirmation_code:
            raise serializers.ValidationError(
                'Error confirmation code.'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]
