from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import VacancyForm, ProfileAvatarForm
from .models import Category, Job, Vacancy, Profile


# ==================== АУТЕНТИФИКАЦИЯ ====================

# Регистрация
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматический вход после регистрации
            login(request, user)
            messages.success(request, f'Аккаунт создан! Добро пожаловать, {user.username}!')
            return redirect('home_page')
        else:
            messages.error(request, 'Ошибка при регистрации. Проверьте данные.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# Вход
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home_page')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# Выход
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('home_page')


# Профиль пользователя
@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    try:
        # Получаем вакансии текущего пользователя
        user_vacancies = Vacancy.objects.filter(author=request.user)

        # Статистика - исправляем статусы согласно вашей модели
        stats = {
            'total_vacancies': user_vacancies.count(),
            'published_vacancies': user_vacancies.filter(status='published').count(),
            'moderation_vacancies': user_vacancies.filter(status='moderation').count(),
            'rejected_vacancies': user_vacancies.filter(status='rejected').count(),
        }

    except Exception as e:
        # Если возникает ошибка, показываем пустые данные
        print(f"Ошибка при получении вакансий: {e}")
        user_vacancies = []
        stats = {
            'total_vacancies': 0,
            'published_vacancies': 0,
            'moderation_vacancies': 0,
            'rejected_vacancies': 0,
        }

    # Обновление профиля
    if request.method == 'POST':
        # Загрузка аватара (если прислали файл)
        if request.FILES.get('avatar'):
            avatar_form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request, 'Аватар успешно обновлен!')
                return redirect('profile')
            else:
                messages.error(request, 'Не удалось загрузить аватар. Проверьте файл.')

        user = request.user
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')

        # Проверка уникальности username
        if new_username and new_username != user.username:
            from django.contrib.auth.models import User
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.error(request, 'Это имя пользователя уже занято')
            else:
                user.username = new_username

        if new_email:
            user.email = new_email
        if new_first_name:
            user.first_name = new_first_name
        if new_last_name:
            user.last_name = new_last_name

        user.save()
        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('profile')

    context = {
        'user_vacancies': user_vacancies,
        'stats': stats,
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'profile.html', context)

# ==================== ВАКАНСИИ ====================

# Список вакансий
def vacancy_list(request):
    vacancies = Vacancy.objects.filter(status='published')
    return render(request, 'vacancy_list.html', {'vacancies': vacancies})


# Просмотр конкретной вакансии
def vacancy_detail(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'vacancy_detail.html', {'vacancy': vacancy})


# Добавление вакансии (только для авторизованных)
@login_required
def vacancy_create(request):
    if request.method == "POST":
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.status = 'moderation'
            vacancy.author = request.user  # Привязываем вакансию к пользователю
            vacancy.save()
            messages.success(request, 'Вакансия отправлена на модерацию!')
            return redirect('home_page')
    else:
        form = VacancyForm()
    return render(request, 'vacancy_form.html', {'form': form})


# Редактирование вакансии (только автор)
@login_required
def vacancy_update(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)

    # Проверяем, что пользователь - автор вакансии
    if vacancy.author != request.user:
        messages.error(request, 'Вы можете редактировать только свои вакансии.')
        return redirect('vacancy_list')

    if request.method == "POST":
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вакансия обновлена!')
            return redirect('vacancy_detail', pk=vacancy.pk)
    else:
        form = VacancyForm(instance=vacancy)
    return render(request, 'vacancy_form.html', {'form': form})


# Удаление вакансии (только автор)
@login_required
def vacancy_delete(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)

    # Проверяем, что пользователь - автор вакансии
    if vacancy.author != request.user:
        messages.error(request, 'Вы можете удалять только свои вакансии.')
        return redirect('vacancy_list')

    if request.method == "POST":
        vacancy.delete()
        messages.success(request, 'Вакансия удалена!')
        return redirect('vacancy_list')
    return render(request, 'vacancy_confirm_delete.html', {'vacancy': vacancy})


# ==================== ДРУГИЕ VIEWS ====================

# Список работ
def job_list(request):
    query = request.GET.get('q')
    salaries = Job.objects.values_list('salary', flat=True).distinct().order_by('salary')
    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(title__icontains=query)

    return render(request, 'job_list.html', {'jobs': jobs, 'salaries': salaries})


# Детали работы
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})


# Главная страница
# views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Vacancy

# views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Vacancy


def home_page(request):
    # Получаем опубликованные вакансии
    vacancies_list = Vacancy.objects.filter(status='published')

    # Фильтрация
    search = request.GET.get('search', '')
    salary = request.GET.get('salary', '')
    experience = request.GET.get('experience', '')

    if search:
        vacancies_list = vacancies_list.filter(
            models.Q(title__icontains=search) |
            models.Q(company__icontains=search)
        )

    if salary:
        vacancies_list = vacancies_list.filter(salary__gte=salary)

    if experience:
        vacancies_list = vacancies_list.filter(experience__gte=experience)

    # ПАГИНАЦИЯ - вот здесь меняйте число!
    paginator = Paginator(vacancies_list, 3)  # ← ИЗМЕНИТЕ 5 на нужное количество
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Уникальные значения для фильтров
    salaries = sorted(set(Vacancy.objects.filter(status='published')
                          .values_list('salary', flat=True)
                          .exclude(salary__isnull=True)))
    experiences = sorted(set(Vacancy.objects.filter(status='published')
                             .values_list('experience', flat=True)
                             .exclude(experience__isnull=True)))

    context = {
        'vacancies': page_obj,  # Для совместимости со старым кодом
        'page_obj': page_obj,  # Для пагинации
        'salaries': salaries,
        'experiences': experiences,
        'selected_salary': salary,
        'selected_experience': experience,
        'search_query': search,
    }

    return render(request, 'home.html', context)


def vacancy_list(request):
    """Страница 'Все вакансии' с пагинацией"""
    # Получаем все опубликованные вакансии
    vacancies_list = Vacancy.objects.filter(status='published')

    # Поиск
    search = request.GET.get('search', '')
    if search:
        vacancies_list = vacancies_list.filter(
            models.Q(title__icontains=search) |
            models.Q(company__icontains=search) |
            models.Q(description__icontains=search)
        )

    # Сортировка по дате (сначала новые)
    vacancies_list = vacancies_list.order_by('-created_at')

    # Пагинация - 12 вакансий на страницу
    paginator = Paginator(vacancies_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'vacancies': page_obj,
        'page_obj': page_obj,
        'search_query': search,
    }

    return render(request, 'vacancy_list.html', context)


# О нас
def about_page(request):
    return render(request, "about.html")


# Контакты
def contact_page(request):
    return render(request, "contact.html")