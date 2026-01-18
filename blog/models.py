from django.contrib.auth.models import User
from django.db import models
from pytils.translit import slugify

class Category(models.Model):
    name = models.CharField("Название категории", max_length=255)
    slug = models.SlugField(unique=True, editable=False, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Job(models.Model):
    title = models.CharField("Название вакансии", max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Выберите категорию")
    company = models.CharField("Название компании", max_length=80)
    experience = models.CharField("Опыт работы", max_length=80, default="без опыта")
    salary = models.CharField("Оклад", max_length=80)
    description = models.TextField("Описание вакансии")
    skills = models.CharField("Навыки", max_length=255)
    address = models.CharField("Адрес", max_length=100, default="адрес компании")
    phone = models.CharField("Номер телефона", max_length=100)
    email = models.CharField("Почта", max_length=100)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title

class Vacancy(models.Model):
    STATUS_CHOICES = [
        ('moderation', 'На модерации'),
        ('published', 'Опубликовано'),
        ('rejected', 'Отклонено'),
    ]
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name='vacancies',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    company = models.CharField(max_length=255, verbose_name="Компания")
    location = models.CharField(max_length=255, verbose_name="Местоположение", default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='moderation', verbose_name="Статус")
    salary = models.CharField(max_length=100, verbose_name="Зарплата", blank=True, null=True)
    experience = models.CharField(max_length=100, verbose_name="Опыт работы", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title

    def get_status_display(self):
        """Возвращает отображаемое имя статуса"""
        for code, name in self.STATUS_CHOICES:
            if code == self.status:
                return name
        return self.status

    def get_status_color(self):
        """Возвращает цвет для статуса"""
        colors = {
            'published': 'success',
            'moderation': 'warning',
            'rejected': 'danger'
        }
        return colors.get(self.status, 'secondary')

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-created_at']

    def __str__(self):
        return self.title