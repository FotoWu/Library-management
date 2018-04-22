from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=40, null=False)
    category = models.CharField(max_length=30)
    press = models.CharField(max_length=40)
    year = models.IntegerField()
    author = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    total = models.IntegerField()
    stock = models.IntegerField()
    class Meta:
        ordering = ['title']

class Card(models.Model):
    TYPE_CHOICES = (
        ('S', 'Student'),
        ('T', 'Teacher'),
    )
    name = models.CharField(max_length=40, null=False)
    dept = models.CharField(max_length=30)
    type = models.CharField(max_length=1, default='S', choices=TYPE_CHOICES)

class User(models.Model):
    password = models.CharField(max_length=16, null=False)
    username = models.CharField(max_length=40, null=False)
    phone_num = models.CharField(max_length=11)

class Borrow(models.Model):
    bid = models.ForeignKey(Book, on_delete=True)
    cid = models.ForeignKey(Card, on_delete=True)
    borrow_date = models.DateField(null=True)
    return_date = models.DateField(null=True)
    manager = models.ForeignKey(User, on_delete=True)