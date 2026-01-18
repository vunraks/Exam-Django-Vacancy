from django.urls import path
from . import views

urlpatterns = [
    # Аутентификация
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Главная и страницы
    path('', views.home_page, name='home_page'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),

    # Вакансии
    path('vacancies/', views.vacancy_list, name='vacancy_list'),
    path('vacancies/<int:pk>/', views.vacancy_detail, name='vacancy_detail'),
    path('vacancies/new/', views.vacancy_create, name='vacancy_create'),
    path('vacancies/<int:pk>/edit/', views.vacancy_update, name='vacancy_update'),
    path('vacancies/<int:pk>/delete/', views.vacancy_delete, name='vacancy_delete'),

    # Работы
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
]