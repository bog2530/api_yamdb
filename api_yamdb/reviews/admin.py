from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')
    list_filter = ('category', 'genre', 'year')
    list_display_links = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'title', 'author', 'score')
    list_filter = ('pub_date', 'author', 'title')
    list_display_links = ('pub_date',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'review', 'author')
    list_filter = ('pub_date', 'author', 'review')
    list_display_links = ('pub_date',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
