import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class Command(BaseCommand):
    dir_path = f'{ settings.BASE_DIR }/static/data/'

    def load_model(self, file_name, model, missed=[]):
        model.objects.all().delete()
        with open(f'{self.dir_path}{file_name}', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                try:
                    missed_counter = 0
                    for empty_ind in missed:
                        row.insert(empty_ind + missed_counter, '')
                        missed_counter += 1
                    new_obj = model(*row)
                    new_obj.save()
                except Exception as r:
                    print(f'{model}: {r}')

    def load_users(self, file_name):
        User.objects.all().delete()
        with open(f'{self.dir_path}{file_name}', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                try:
                    user = User.objects.create_user(
                        pk=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6],
                        password=User.objects.make_random_password()
                    )
                    user.save()
                except Exception as r:
                    print(f'{self.load_users.__name__}: {r}')

    def load_genres_titles(self, file_name):
        with open(f'{self.dir_path}{file_name}', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                try:
                    title = Title.objects.get(pk=row[1])
                    genre = Genre.objects.get(pk=row[2])
                    title.genre.add(genre)
                    title.save()
                except Exception as r:
                    print(f'{self.load_genres_titles.__name__}: {r}')

    def handle(self, *args, **options):
        self.load_users('users.csv')
        self.load_model('category.csv', Category)
        self.load_model('genre.csv', Genre)
        self.load_model('titles.csv', Title, missed=[3])
        self.load_genres_titles('genre_title.csv')
        self.load_model('review.csv', Review)
        self.load_model('comments.csv', Comment)
