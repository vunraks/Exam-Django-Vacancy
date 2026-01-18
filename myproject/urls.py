from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Аутентификация
    path('register/', blog_views.register_view, name='register'),  # исправлено
    path('login/', blog_views.login_view, name='login'),  # исправлено
    path('logout/', blog_views.logout_view, name='logout'),  # исправлено
    path('profile/', blog_views.profile_view, name='profile'),  # исправлено

    # Основные маршруты блога
    path('', include('blog.urls')),
]