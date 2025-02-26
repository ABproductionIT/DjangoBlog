from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from blog import views
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Детальная страница поста
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('admin/', admin.site.urls),
    path('images/<str:filename>/', views.image_view, name='image_view'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]