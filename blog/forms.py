from django import forms
from .models import Vacancy, Profile


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


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
