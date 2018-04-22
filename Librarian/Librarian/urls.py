"""Librarian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from library import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login, name='login'),
    url(r'^login/', views.login, name='login'),
    url(r'^home/$', views.home, name='home'),
    url(r'^add_book/$', views.add_book, name='add_book'),
    url(r'^borrow_return/$', views.borrow_return, name='borrow_return'),
    url(r'^return_book.html$', views.return_book, name='return_book'),
    url(r'^borrow_book/$', views.borrow_book, name='borrow_book'),
    url(r'^manage_card/$', views.manage_card, name='manage_card'),
    url(r'^delete_card.html$', views.delete_card, name='delete_card'),
    url(r'^search/$', views.search, name='search'),
]