from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput
from .models import Customer, City, Organization, Category, Vacancy, Respond 
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('title',)
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('title',)
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('title',)
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('datev', 'city', 'organization', 'category', 'position', 'details', 'salary')
        widgets = {
            'datev': DateInput(attrs={"type":"date"}),
            'city': forms.Select(attrs={'class': 'chosen'}),
            'organization': forms.Select(attrs={'class': 'chosen'}),
            'category': forms.Select(attrs={'class': 'chosen'}),
            'position': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 50, 'rows': 5}),
            'salary': TextInput(attrs={"size":"0"}),
        }
        labels = {
            'city': _('city'),
            'organization': _('organization'),
            'category': _('category'),
        }

class VacancyCloseForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('datev', 'city', 'organization', 'category', 'position', 'details', 'salary', 'date_close', 'date_close')
        widgets = {
            'datev': DateInput(attrs={"type":"date", "readonly":"readonly"}),
            'city': forms.Select(attrs={"disabled": "true"}),
            'organization': forms.Select(attrs={"disabled": "true"}),
            'category': forms.Select(attrs={"disabled": "true"}),
            'position': TextInput(attrs={"size":"100", "readonly":"readonly"}),
            'details': Textarea(attrs={'cols': 50, 'rows': 5, "readonly":"readonly"}),
            'salary': TextInput(attrs={"size":"0", "readonly":"readonly"}),
            'date_close': DateInput(attrs={"type":"date"}),
        }
        labels = {
            'city': _('city'),
            'organization': _('organization'),
            'category': _('category'),
        }

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

