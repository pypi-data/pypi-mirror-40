from django.contrib import admin

from .models import Post, PostPhoto


class PostPhotoInline(admin.TabularInline):
    model = PostPhoto
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'created',
        'updated',
    ]

    list_filter = [
        'created',
    ]

    search_fields = [
        'title',
        'subtitle',
        'body',
    ]

    prepopulated_fields = {
        'slug': ['title'],
    }

    readonly_fields = [
        'created',
        'updated',
    ]

    inlines = [
        PostPhotoInline,
    ]
