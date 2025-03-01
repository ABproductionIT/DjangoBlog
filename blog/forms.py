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
    main_image = forms.ImageField(required=False)  # Поле загрузки изображений

    class Meta:
        model = Post
        fields = ['title', 'content', 'main_image', 'publication_date', 'posted', 'author']

    def __init__(self, *args, **kwargs):
        """
        Если у поста уже есть изображение (BinaryField), создаем объект файла,
        чтобы Django корректно отображал его в админке.
        """
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.main_image:
            # Преобразуем binary (memoryview) в bytes
            image_bytes = bytes(self.instance.main_image)
            self.fields['main_image'].initial = SimpleUploadedFile("current_image.png", image_bytes)

    def clean_main_image(self):
        """
        Конвертирует загружаемое изображение в бинарные данные перед сохранением.
        """
        image = self.cleaned_data.get('main_image')

        if isinstance(image, forms.FileField):
            return image.read()  # Если это новый файл, читаем его в байты

        if isinstance(image, memoryview):
            return bytes(image)  # Если уже сохраненное изображение — memoryview, конвертируем в байты

        if self.instance and isinstance(self.instance.main_image, memoryview):
            return bytes(self.instance.main_image)  # Оставляем старое изображение, если нового нет

        return None  # Если изображения нет вообще