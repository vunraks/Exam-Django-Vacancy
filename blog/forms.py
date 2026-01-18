from django import forms
from .models import Vacancy


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'description', 'company', 'location', 'salary', 'experience']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'company': 'Компания',
            'location': 'Местоположение',
            'salary': 'Зарплата',
            'experience': 'Опыт работы',
        }
