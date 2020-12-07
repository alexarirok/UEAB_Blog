from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name='profile'),
    path('blog/', views.blog, name='post-list'),
    path('post/<id>/', views.post, name='post-detail'),
    path('search/', views.search, name='search'),
    path('create/', views.post_create, name='post-create'),
    path('post/<id>/update/', views.post_update, name='post_update'),
    path('post/<id>/delete', views.post_delete, name='post_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)