from django.contrib import admin
from django.utils.html import format_html

from .models import Post, PostImage, SiteInfo
from .forms import PostImageAdminForm

from django.contrib import admin
from .models import Post
from .forms import PostAdminForm
import base64
from django.utils.html import format_html

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm  # Используем кастомную форму

    def main_image_preview(self, obj):
        """
        Отображает превью изображения в админке.
        """
        if obj.main_image:
            img_base64 = base64.b64encode(obj.main_image).decode('utf-8')
            return format_html(f'<img src="data:image/png;base64,{img_base64}" width="100" />')
        return "Нет изображения"

    main_image_preview.allow_tags = True
    main_image_preview.short_description = "Превью"

    list_display = ('title', 'posted', 'publication_date', 'main_image_preview')
    readonly_fields = ('main_image_preview',)  # Добавляем превью в карточку редактирования

admin.site.register(Post, PostAdmin)



@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        """Запрещает добавление новой записи, если уже есть одна."""
        if SiteInfo.objects.exists():
            return False
        return super().has_add_permission(request)


class PostImageAdmin(admin.ModelAdmin):
    form = PostImageAdminForm  # Используем кастомную форму

    def image_preview(self, obj):
        """
        Отображает превью изображения в админке.
        """
        if obj.image:
            import base64
            from django.utils.html import format_html
            img_base64 = base64.b64encode(obj.image).decode('utf-8')
            return format_html(f'<img src="data:image/png;base64,{img_base64}" width="100" />')
        return "Нет изображения"

    image_preview.allow_tags = True
    image_preview.short_description = "Превью"

    list_display = ('tag', 'image_preview')

admin.site.register(PostImage, PostImageAdmin)

