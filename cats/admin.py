from django.contrib import admin
from .models import Cat, Comment, Reaction


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'coat_color', 'is_public', 'created_on')
    list_filter = ('is_public', 'coat_color', 'created_on')
    search_fields = ('name', 'personality', 'owner__username')
    list_editable = ('is_public',)  # quickly hide a cat without deleting it


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('cat', 'author', 'body', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('body', 'author__username', 'cat__name')


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('cat', 'user', 'created_on')
