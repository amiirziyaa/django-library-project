from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'price', 'category', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان کتاب'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام نویسنده'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مثلا 1390'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مثلا 250000'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'genres': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }