from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Подключение моделей
from .models import Customer, City, Organization, Category, Vacancy, Respond 
# Подключение форм
from .forms import CityForm, OrganizationForm, CategoryForm, VacancyForm, VacancyCloseForm, SignUpForm

import datetime

from django.db import models

import sys

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.shortcuts import get_object_or_404

import random


# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

# Стартовая страница
#@login_required 
def index(request):
    return render(request, "index.html")

# Страница Контакты
def contact(request):
    return render(request, "contact.html")

# Страница Отчеты
@login_required
@group_required("Managers")
def report(request):
    if request.method == "POST":
        print(request.POST.get("reportMode"))
        if (request.POST.get("reportMode") == "Vacancy"):
            vacancy = Vacancy.objects.all().order_by('-datev')
            return render(request, "report.html", {"vacancy": vacancy })            
        elif (request.POST.get("reportMode") == "Respond"):
            respond = Respond.objects.all().order_by('-dater')
            return render(request, "report.html", {"respond": respond })              
        elif (request.POST.get("reportMode") == "Customer"):
            customer = Customer.objects.all().order_by('fio')
            return render(request, "report.html", {"customer": customer })              
        else:
            print("Error")
    else:
        return render(request, "report.html")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def city_index(request):
    city = City.objects.all().order_by('title')
    return render(request, "city/index.html", {"city": city})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def city_create(request):
    if request.method == "POST":
        city = City()        
        city.title = request.POST.get("title")
        city.save()
        return HttpResponseRedirect(reverse('city_index'))
    else:        
        cityform = CityForm(request.FILES)
        return render(request, "city/create.html", {"form": cityform})

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def city_edit(request, id):
    try:
        city = City.objects.get(id=id) 
        if request.method == "POST":
            city.title = request.POST.get("title")
            city.save()
            return HttpResponseRedirect(reverse('city_index'))
        else:
            # Загрузка начальных данных
            cityform = CityForm(initial={'title': city.title, })
            return render(request, "city/edit.html", {"form": cityform})
    except City.DoesNotExist:
        return HttpResponseNotFound("<h2>City not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def city_delete(request, id):
    try:
        city = City.objects.get(id=id)
        city.delete()
        return HttpResponseRedirect(reverse('city_index'))
    except City.DoesNotExist:
        return HttpResponseNotFound("<h2>City not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def city_read(request, id):
    try:
        city = City.objects.get(id=id) 
        return render(request, "city/read.html", {"city": city})
    except City.DoesNotExist:
        return HttpResponseNotFound("<h2>City not found</h2>")    

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def organization_index(request):
    organization = Organization.objects.all().order_by('title')
    return render(request, "organization/index.html", {"organization": organization})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def organization_create(request):
    if request.method == "POST":
        organization = Organization()        
        organization.title = request.POST.get("title")
        organization.save()
        return HttpResponseRedirect(reverse('organization_index'))
    else:        
        organizationform = OrganizationForm(request.FILES)
        return render(request, "organization/create.html", {"form": organizationform})

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def organization_edit(request, id):
    try:
        organization = Organization.objects.get(id=id) 
        if request.method == "POST":
            organization.title = request.POST.get("title")
            organization.save()
            return HttpResponseRedirect(reverse('organization_index'))
        else:
            # Загрузка начальных данных
            organizationform = OrganizationForm(initial={'title': organization.title, })
            return render(request, "organization/edit.html", {"form": organizationform})
    except Organization.DoesNotExist:
        return HttpResponseNotFound("<h2>Organization not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def organization_delete(request, id):
    try:
        organization = Organization.objects.get(id=id)
        organization.delete()
        return HttpResponseRedirect(reverse('organization_index'))
    except Organization.DoesNotExist:
        return HttpResponseNotFound("<h2>Organization not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def organization_read(request, id):
    try:
        organization = Organization.objects.get(id=id) 
        return render(request, "organization/read.html", {"organization": organization})
    except Organization.DoesNotExist:
        return HttpResponseNotFound("<h2>Organization not found</h2>")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def category_index(request):
    category = Category.objects.all().order_by('title')
    return render(request, "category/index.html", {"category": category})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def category_create(request):
    if request.method == "POST":
        category = Category()        
        category.title = request.POST.get("title")
        category.save()
        return HttpResponseRedirect(reverse('category_index'))
    else:        
        categoryform = CategoryForm(request.FILES)
        return render(request, "category/create.html", {"form": categoryform})

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def category_edit(request, id):
    try:
        category = Category.objects.get(id=id) 
        if request.method == "POST":
            category.title = request.POST.get("title")
            category.save()
            return HttpResponseRedirect(reverse('category_index'))
        else:
            # Загрузка начальных данных
            categoryform = CategoryForm(initial={'title': category.title, })
            return render(request, "category/edit.html", {"form": categoryform})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def category_delete(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return HttpResponseRedirect(reverse('category_index'))
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def category_read(request, id):
    try:
        category = Category.objects.get(id=id) 
        return render(request, "category/read.html", {"category": category})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")


# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def vacancy_index(request):
    vacancy = Vacancy.objects.all().order_by('-datev')
    return render(request, "vacancy/index.html", {"vacancy": vacancy})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def vacancy_create(request):
    if request.method == "POST":
        vacancy = Vacancy()        
        vacancy.datev = request.POST.get("datev")
        vacancy.city = City.objects.filter(id=request.POST.get("city")).first()
        vacancy.organization = Organization.objects.filter(id=request.POST.get("organization")).first()
        vacancy.category = Category.objects.filter(id=request.POST.get("category")).first()
        vacancy.position = request.POST.get("position")
        vacancy.details = request.POST.get("details")
        vacancy.salary = request.POST.get("salary")
        vacancy.save()
        return HttpResponseRedirect(reverse('vacancy_index'))
    else:        
        vacancyform = VacancyForm(initial={'datev': datetime.datetime.now().strftime('%Y-%m-%d'), })
        return render(request, "vacancy/create.html", {"form": vacancyform})

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def vacancy_edit(request, id):
    try:
        vacancy = Vacancy.objects.get(id=id) 
        if request.method == "POST":
            vacancy.datev = request.POST.get("datev")
            vacancy.city = City.objects.filter(id=request.POST.get("city")).first()
            vacancy.organization = Organization.objects.filter(id=request.POST.get("organization")).first()
            vacancy.category = Category.objects.filter(id=request.POST.get("category")).first()
            vacancy.position = request.POST.get("position")
            vacancy.details = request.POST.get("details")
            vacancy.salary = request.POST.get("salary")
            vacancy.save()
            return HttpResponseRedirect(reverse('vacancy_index'))
        else:
            # Загрузка начальных данных
            vacancyform = VacancyForm(initial={'datev': vacancy.datev.strftime('%Y-%m-%d'), 'city': vacancy.city, 'organization': vacancy.organization, 'category': vacancy.category, 'position': vacancy.position, 'details': vacancy.details, 'salary': vacancy.salary,  })
            return render(request, "vacancy/edit.html", {"form": vacancyform})
    except Vacancy.DoesNotExist:
        return HttpResponseNotFound("<h2>Vacancy not found</h2>")

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def vacancy_close(request, id):
    try:
        vacancy = Vacancy.objects.get(id=id) 
        if request.method == "POST":
            vacancy.date_close = request.POST.get("date_close")
            vacancy.save()
            return HttpResponseRedirect(reverse('vacancy_index'))
        else:
            # Загрузка начальных данных
            vacancyform = VacancyCloseForm(initial={'datev': vacancy.datev.strftime('%Y-%m-%d'), 'city': vacancy.city, 'organization': vacancy.organization, 'category': vacancy.category, 'position': vacancy.position, 'details': vacancy.details, 'salary': vacancy.salary, 'date_close': vacancy.date_close, })
            return render(request, "vacancy/edit.html", {"form": vacancyform})
    except Vacancy.DoesNotExist:
        return HttpResponseNotFound("<h2>Vacancy not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def vacancy_delete(request, id):
    try:
        vacancy = Vacancy.objects.get(id=id)
        vacancy.delete()
        return HttpResponseRedirect(reverse('vacancy_index'))
    except Vacancy.DoesNotExist:
        return HttpResponseNotFound("<h2>Vacancy not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def vacancy_read(request, id):
    try:
        vacancy = Vacancy.objects.get(id=id) 
        return render(request, "vacancy/read.html", {"vacancy": vacancy})
    except Vacancy.DoesNotExist:
        return HttpResponseNotFound("<h2>Vacancy not found</h2>")
    
# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    #fields = ('first_name', 'last_name', 'email',)
    fields = ('email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user



