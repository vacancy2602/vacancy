"""vacancy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings 
from django.conf.urls.static import static 
from django.conf.urls import include

from quest import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('report/', views.report, name='report'),        
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('category/index/', views.category_index, name='category_index'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('category/read/<int:id>/', views.category_read, name='category_read'),

    path('city/index/', views.city_index, name='city_index'),
    path('city/create/', views.city_create, name='city_create'),
    path('city/edit/<int:id>/', views.city_edit, name='city_edit'),
    path('city/delete/<int:id>/', views.city_delete, name='city_delete'),
    path('city/read/<int:id>/', views.city_read, name='city_read'),

    path('organization/index/', views.organization_index, name='organization_index'),
    path('organization/create/', views.organization_create, name='organization_create'),
    path('organization/edit/<int:id>/', views.organization_edit, name='organization_edit'),
    path('organization/delete/<int:id>/', views.organization_delete, name='organization_delete'),
    path('organization/read/<int:id>/', views.organization_read, name='organization_read'),

    path('vacancy/index/', views.vacancy_index, name='vacancy_index'),
    path('vacancy/create/', views.vacancy_create, name='vacancy_create'),
    path('vacancy/edit/<int:id>/', views.vacancy_edit, name='vacancy_edit'),
    path('vacancy/close/<int:id>/', views.vacancy_close, name='vacancy_close'),
    path('vacancy/delete/<int:id>/', views.vacancy_delete, name='vacancy_delete'),
    path('vacancy/read/<int:id>/', views.vacancy_read, name='vacancy_read'),
    
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

