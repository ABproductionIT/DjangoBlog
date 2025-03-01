from django.shortcuts import render, get_object_or_404
from .models import Post, PostImage, SiteInfo
import re
import base64
from django.utils.safestring import mark_safe
from django.http import HttpResponse, Http404
import mimetypes


def find_image_tags(content):
    """
    Находит все теги $imageN$ в переданном тексте.
    """
    regex = r"\$image\d+\$"  # Регулярное выражение для поиска $imageN$
    matches = re.findall(regex, content)  # Находим все совпадения
    return matches if matches else []  # Если совпадений нет, возвращаем пустой список


def replace_image_tags(content, images_dict):
    """
    Заменяет теги $imageN$ в тексте на <img src="data:image/png;base64,..." >
    """

    def replacer(match):
        tag = match.group(0)  # Найденный $imageN$
        img_base64 = images_dict.get(tag, None)
        if img_base64:
            return f'<p> <img src="data:image/png;base64,{img_base64}" alt="\n🖼\n"> </p>'
        return tag  # Если изображения нет, оставляем как есть

    regex = r"\$image\d+\$"  # Регулярное выражение для поиска $imageN$
    return mark_safe(re.sub(regex, replacer, content))


def post_detail(request, pk):
    ret_post_img_dict = {}
    post = get_object_or_404(Post, pk=pk)

    # Находим все теги вида $imageN$
    tags = find_image_tags(post.content)

    # Получаем изображения из базы
    p_img = PostImage.objects.filter(tag__in=tags)

    # Кодируем в base64 и добавляем в словарь
    for el in p_img:
        ret_post_img_dict[el.tag] = base64.b64encode(el.image).decode('utf-8')

    # Заменяем теги $imageN$ на изображения
    new_content = replace_image_tags(post.content, ret_post_img_dict)

    return render(request, 'post.html', {'post': post, 'content': new_content})

def image_view(request, post_id):
    """
    Отдает изображение из базы данных по ID поста.
    """
    post = get_object_or_404(Post, id=post_id)

    if not post.main_image:
        raise Http404("Изображение не найдено")

    # Определяем MIME-тип (если известен)
    content_type, _ = mimetypes.guess_type("image.png")  # Меняйте на image/jpeg, если используете JPG
    return HttpResponse(post.main_image, content_type=content_type)