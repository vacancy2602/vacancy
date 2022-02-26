from django.contrib import admin

from .models import Customer, City, Organization, Category, Vacancy, Respond 

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Customer)
admin.site.register(City)
admin.site.register(Organization)
admin.site.register(Category)
admin.site.register(Vacancy)
admin.site.register(Respond)
