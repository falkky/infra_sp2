from django.contrib import admin

from .models import (Categories, Comments, Genres, GenresTitles,
                     Review, Title, User)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role',)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)


class GenresAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category', 'get_genre')
    search_fields = ('name', 'description',)
    list_filter = ('year', 'genre', 'category',)
    empty_value_display = '-пусто-'

    def get_genre(self, obj):
        return ', '.join([g.name for g in obj.genre.all()])


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author',)
    search_fields = ('text',)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text',)
    search_fields = ('text',)


class GenresTitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'genre')


admin.site.register(User, UserAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(GenresTitles, GenresTitlesAdmin)
