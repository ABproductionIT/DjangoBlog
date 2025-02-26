from django.db import models
from django.contrib.auth.models import User  # если author — пользователь
from django.core.exceptions import ValidationError

class SiteInfo(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название сайта")
    description = models.TextField(verbose_name="Краткое описание")

    def save(self, *args, **kwargs):
        if SiteInfo.objects.exists() and not self.pk:
            raise ValidationError("Можно создать только одну запись SiteInfo.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Информация о сайте"
        verbose_name_plural = "Информация о сайте"


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    main_image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    # Дата публикации, которую можно выбирать вручную (не устанавливается автоматически)
    publication_date = models.DateTimeField(null=True, blank=True, help_text="Выберите дату публикации")
    # Флажок: опубликован пост или нет
    posted = models.BooleanField(default=False, help_text="Если отмечено, пост виден всем")
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def can_view(self, user):
        """
        Если пост опубликован (posted == True) — виден всем,
        иначе (posted == False) виден только суперпользователям.
        """
        return self.posted or (user.is_authenticated and user.is_superuser)

    def __str__(self):
        return self.title

class PostImage(models.Model):
    image = models.ImageField(upload_to='post_images/')
    tag = models.CharField(max_length=20, blank=True, unique=True)

    def save(self, *args, **kwargs):
        """
        Автоматически устанавливает tag в формате $imageN$ перед сохранением.
        """
        if not self.tag:
            last_image = PostImage.objects.order_by('-id').first()
            next_id = (last_image.id + 1) if last_image else 1
            self.tag = f"$image{next_id}$"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tag}"

