# library/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .models import Book, Category, Genre, Shelf
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required



class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(author__icontains=search_query)
            )
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        start_year = self.request.GET.get('start_year', '')
        end_year = self.request.GET.get('end_year', '')
        category_id = self.request.GET.get('category', '')
        genre_id = self.request.GET.get('genre', '')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if start_year:
            queryset = queryset.filter(publication_year__gte=start_year)
        if end_year:
            queryset = queryset.filter(publication_year__lte=end_year)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['start_year'] = self.request.GET.get('start_year', '')
        context['end_year'] = self.request.GET.get('end_year', '')
        context['categories'] = Category.objects.all()
        context['category_id'] = self.request.GET.get('category', '')
        context['genres'] = Genre.objects.all()
        context['genre_id'] = self.request.GET.get('genre', '')
        if self.request.user.is_authenticated:
            context['user_shelves'] = Shelf.objects.filter(owner=self.request.user)
        return context


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'library/book_form.html'
    fields = ['title', 'author', 'publication_year', 'price', 'category', 'genres']
    success_url = reverse_lazy('book_list')


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'library/book_form.html'
    fields = ['title', 'author', 'publication_year', 'price', 'category', 'genres']
    success_url = reverse_lazy('book_list')


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'library/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')


@login_required
def delete_filtered_books(request):
    if request.method == 'POST':
        queryset = Book.objects.all()
        search_query = request.POST.get('q', '')
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query))
        min_price = request.POST.get('min_price', '')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        queryset.delete()
    return redirect('book_list')



class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        user = request.user
        if book in user.favorite_books.all():
            user.favorite_books.remove(book)
        else:
            user.favorite_books.add(book)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class FavoriteBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'library/favorite_book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        return self.request.user.favorite_books.all()



class UserShelfListView(LoginRequiredMixin, ListView):
    model = Shelf
    template_name = 'library/user_shelf_list.html'
    context_object_name = 'shelves'

    def get_queryset(self):
        return Shelf.objects.filter(owner=self.request.user)


class ShelfDetailView(LoginRequiredMixin, DetailView):
    model = Shelf
    template_name = 'library/shelf_detail.html'
    context_object_name = 'shelf'

    def get_queryset(self):
        return Shelf.objects.filter(owner=self.request.user)


class ShelfCreateView(LoginRequiredMixin, CreateView):
    model = Shelf
    fields = ['name']
    template_name = 'library/shelf_form.html'
    success_url = reverse_lazy('user_shelf_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AddBookToShelfView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        book_pk = self.kwargs['book_pk']
        shelf_pk = request.POST.get('shelf')
        book = get_object_or_404(Book, pk=book_pk)
        shelf = get_object_or_404(Shelf, pk=shelf_pk, owner=request.user)
        shelf.books.add(book)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('book_list')))


class RemoveBookFromShelfView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        shelf_pk = self.kwargs['shelf_pk']
        book_pk = self.kwargs['book_pk']
        shelf = get_object_or_404(Shelf, pk=shelf_pk, owner=request.user)
        book = get_object_or_404(Book, pk=book_pk)
        shelf.books.remove(book)
        return HttpResponseRedirect(reverse('shelf_detail', kwargs={'pk': shelf_pk}))



class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'library/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_object'] = self.request.user
        return context
class ShelfDeleteView(LoginRequiredMixin, DeleteView):
    model = Shelf
    template_name = 'library/shelf_confirm_delete.html'
    success_url = reverse_lazy('user_shelf_list')

    def get_queryset(self):
        return Shelf.objects.filter(owner=self.request.user)