from django.contrib import admin
from .models import Job, Category, Vacancy  # Все модели в одном импорте

# Регистрация модели Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

# Регистрация модели Job
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'salary', 'experience')
    list_filter = ('category', 'company')
    search_fields = ('title', 'company', 'description')
    list_per_page = 20

# Регистрация модели Vacancy
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'status', 'salary', 'experience')
    list_filter = ('status', 'company')
    search_fields = ('title', 'company', 'description')
    list_editable = ('status',)
    actions = ['approve_vacancies', 'reject_vacancies']

    def approve_vacancies(self, request, queryset):
        queryset.update(status='published')
        self.message_user(request, f"{queryset.count()} вакансий одобрено")
    approve_vacancies.short_description = "Одобрить выбранные вакансии"

    def reject_vacancies(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} вакансий отклонено")
    reject_vacancies.short_description = "Отклонить выбранные вакансии"