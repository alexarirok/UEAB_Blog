
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from posts.views import login_view, register_view, logout_view, signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('tinymce/', include('tinymce.urls')),
    # path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html')),
    path('accounts/register/', signup, name='register'),
    path('accounts/login/', login_view, name='login' ),
    path('social-auth/', include('social_django.urls', namespace="social")),
    # path('accounts/register/', register_view),
    # path('accounts/logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('logout/',logout_view, name='logout'),
]
