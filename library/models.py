# library/models.py

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='نام ژانر')

    class Meta:
        verbose_name = "ژانر"
        verbose_name_plural = "ژانر ها"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان کتاب")
    author = models.CharField(max_length=150, verbose_name="نویسنده")
    publication_year = models.IntegerField(null=True, blank=True, verbose_name="سال انتشار")
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="قیمت")

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دسته‌بندی")
    genres = models.ManyToManyField(Genre, blank=True, verbose_name="ژانر(ها)")
    favorited_by = models.ManyToManyField(User, related_name='favorite_books', blank=True)

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب‌ها"
        ordering = ['-id']

    def __str__(self):
        return f"{self.title} - {self.author}"

    def get_absolute_url(self):
        return reverse('book_list')


class Shelf(models.Model):
    name = models.CharField(max_length=150, verbose_name="نام قفسه")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shelves", verbose_name="صاحب")
    books = models.ManyToManyField(Book, blank=True, related_name="shelves", verbose_name="کتاب‌ها")

    class Meta:
        verbose_name = "قفسه"
        verbose_name_plural = "قفسه‌ها"
        unique_together = ('name', 'owner')

    def __str__(self):
        return f"{self.name} (متعلق به {self.owner.username})"

