from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category',)
    list_filter = ('name', 'year', 'genre', 'category',)


class CategoryAdmn(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date')
    list_editable = ('text', )
    ordering = ('pub_date', )
    list_per_page = 10
    search_fields = ('author__email', 'autor__username', 'title__name')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'text', 'author', 'pub_date')
    list_editable = ('text', )
    ordering = ('pub_date', )
    list_per_page = 10
    search_fields = ('author__email', 'autor__username', 'review__title__name')


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmn)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
