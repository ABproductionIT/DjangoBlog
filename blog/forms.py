from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import PostImage, Post

class PostImageAdminForm(forms.ModelForm):
    image = forms.ImageField()  # Используем ImageField для удобного выбора файла

    class Meta:
        model = PostImage
        fields = ['image', 'tag']

    def clean_image(self):
        """
        Переводим изображение в бинарные данные перед сохранением.
        """
        image = self.cleaned_data.get('image')
        if image:
            return image.read()  # Преобразуем изображение в bytes
        return image


class PostAdminForm(forms.ModelForm):
    main_image = forms.ImageField()  # Поле загрузки изображения

    class Meta:
        model = Post
        fields = ['title', 'content', 'main_image', 'publication_date', 'posted', 'author']

    def clean_main_image(self):
        """
        Конвертирует загружаемое изображение в бинарные данные перед сохранением.
        """
        image = self.cleaned_data.get('main_image')
        if image:
            return image.read()  # Преобразуем изображение в бинарный формат
        return image