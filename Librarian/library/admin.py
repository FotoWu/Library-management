from django.contrib import admin
from library.models import Book, Card, User, Borrow

# Register your models here.
admin.site.register([Book, Card, User, Borrow])