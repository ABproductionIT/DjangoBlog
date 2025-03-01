from django.shortcuts import render, get_object_or_404
from .models import Post, PostImage, SiteInfo
import re
from django.utils.safestring import mark_safe
from django.http import HttpResponse, Http404
import mimetypes


def find_image_tags(content):
    """
    Находит все теги $imageN$ в переданном тексте.

    :param content: строка с текстом, содержащая теги $imageN$
    :return: список найденных тегов
    """
    regex = r"\$image\d+\$"  # Регулярное выражение для поиска $imageN$
    matches = re.findall(regex, content)  # Находим все совпадения
    return matches if matches else []  # Если совпадений нет, возвращаем пустой список


def replace_image_tags(content, images_dict):
    """
    Заменяет теги $imageN$ в тексте на <img src="URL">

    :param content: строка с текстом
    :param images_dict: словарь {"$image1$": "URL1", "$image2$": "URL2"}
    :return: текст с замененными изображениями
    """

    def replacer(match):
        tag = match.group(0)  # Найденный $imageN$

        return f'<p> <img src="{images_dict.get(tag, "#")}" alt="\n🖼\n"> </p>'  # Если нет URL, подставляем #

    regex = r"\$image\d+\$"  # Регулярное выражение для поиска $imageN$
    return mark_safe(re.sub(regex, replacer, content))


def index(request):
    site_name_info=SiteInfo.objects.all().last()
    if site_name_info:
        title = site_name_info.title
        description = site_name_info.description
    else:
        title, description  = "DjangoBlog", "Simple blog project on Django"
    posts = Post.objects.filter(posted=True)  # выводим только опубликованные посты
    return render(request, 'index.html', {'posts': posts, 'site_name': title, 'description': description})

def post_detail(request, pk):
    ret_post_img_dict = {}
    post = get_object_or_404(Post, pk=pk)
    tags = find_image_tags(post.content)
    p_img = PostImage.objects.filter(tag__in=tags)
    for el in p_img:
        ret_post_img_dict[el.tag] = el.image.url
    print(ret_post_img_dict)

    new_content = replace_image_tags(post.content, ret_post_img_dict)
    print(new_content)

    return render(request, 'post.html', {'post': post, 'content': new_content})


def image_view(request, post_id):
    """
    Отдает изображение из базы данных по ID поста.
    """
    post = get_object_or_404(Post, id=post_id)

    if not post.main_image:
        raise Http404("Изображение не найдено")

    # Определяем MIME-тип (по умолчанию image/png)
    content_type, _ = mimetypes.guess_type("image.png")  # Можно менять на "image/jpeg", если нужны JPG
    return HttpResponse(post.main_image, content_type=content_type)