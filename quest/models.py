from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Пользователь клиент
class Customer(models.Model):
    telegram_id = models.IntegerField(_('telegram_id'))     # id пользователя Telegram
    phone_number = models.CharField(_('phone_number'), max_length=20)    
    first_name = models.CharField(_('first_name'), max_length=64)
    last_name = models.CharField(_('last_name'), blank=True, null=True, max_length=64)
    fio = models.CharField(_('fio'), max_length=196, blank=True, null=True)
    birthday = models.DateTimeField(_('birthday'), blank=True, null=True)
    education = models.TextField(_('education'), blank=True, null=True)
    experience = models.TextField(_('experience'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'customer'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['telegram_id']),
            models.Index(fields=['phone_number']),
        ]
        # Сортировка по умолчанию
        ordering = ['first_name', 'last_name', 'phone_number']        
    def __str__(self):
        # Вывод в тег Select
        return "{} ({})".format(self.phone_number, self.first_name)    
    @property
    def info(self):
        # Возврат информации
        return '%s: %s' % (self.fio, self.phone_number)

# Город
class City(models.Model):
    title = models.CharField(_('title_city'), unique=True, max_length=196)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'city'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод Название в тег SELECT 
        return self.title

# Организация
class Organization(models.Model):
    title = models.CharField(_('title_organization'), max_length=196)
    details = models.TextField(_('organization_details'), blank=True, null=True)
    address = models.CharField(_('address'), max_length=128)
    phone = models.CharField(_('phone'), max_length=128)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'organization'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод в тег Select
        return "{}".format(self.title)

# Категория (вид деятельности)
class Category(models.Model):
    title = models.CharField(_('title_category'), unique=True, max_length=196)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'category'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод Название в тег SELECT 
        return self.title

# Вакансия
class Vacancy(models.Model):
    datev = models.DateTimeField(_('datev'))
    city = models.ForeignKey(City, related_name='vacancy_city', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='vacancy_organization', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='vacancy_category', on_delete=models.CASCADE)    
    position = models.CharField(_('position'), max_length=196)
    details = models.TextField(_('vacancy_details'))
    salary = models.CharField(_('salary'), max_length=196)
    date_close = models.DateTimeField(_('date_close'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'vacancy'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['organization']),
            models.Index(fields=['category']),
        ]
        # Сортировка по умолчанию
        ordering = ['datev']
    def __str__(self):
        # Вывод Название в тег SELECT 
        return self.title
    @property
    def info(self):
        # Возврат информации
        return '%s, %s, %s: %s' % (self.city, self.organization, self.category, self.position)
   
# Отклик на вакансию
class Respond(models.Model):
    dater = models.DateTimeField(_('dater'), auto_now_add=True)
    vacancy = models.ForeignKey(Vacancy, related_name='respond_vacancy', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='respond_customer', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'respond'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['vacancy']),
            models.Index(fields=['customer']),
        ]
        # Сортировка по умолчанию
        ordering = ['dater']
    def __str__(self):
        # Вывод Название в тег SELECT 
        return self.vacancy
