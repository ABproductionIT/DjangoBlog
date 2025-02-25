from django.contrib import admin
from django.utils.html import format_html

from .models import Post, PostImage

admin.site.register(Post)


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'preview_image')

    def preview_image(self, obj):
        """Отображение превью изображения в админке."""
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;"/>',
                obj.image.url
            )
        return "Нет изображения"

    preview_image.short_description = "Превью"

