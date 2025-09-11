# library/urls.py

from django.urls import path
from .views import (
    BookListView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    delete_filtered_books,
    ToggleFavoriteView,
    FavoriteBookListView,
    UserShelfListView,
    ShelfDetailView,
    ShelfCreateView,
    AddBookToShelfView,
    UserProfileView,
    RemoveBookFromShelfView,
    ShelfDeleteView,
)

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),

    path('book/add/', BookCreateView.as_view(), name='book_add'),

    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),

    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),

    path('delete-filtered/', delete_filtered_books, name='delete_filtered'),
    path('book/<int:pk>/favorite/', ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('favorites/', FavoriteBookListView.as_view(), name='favorite_list'),
    path('shelves/', UserShelfListView.as_view(), name='user_shelf_list'),
    path('shelves/create/', ShelfCreateView.as_view(), name='shelf_create'),
    path('shelves/<int:pk>/', ShelfDetailView.as_view(), name='shelf_detail'),
    path('book/<int:book_pk>/add-to-shelf/', AddBookToShelfView.as_view(), name='add_to_shelf'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('shelf/<int:shelf_pk>/remove-book/<int:book_pk>/', RemoveBookFromShelfView.as_view(),
         name='remove_from_shelf'),
    path('shelves/<int:pk>/delete/', ShelfDeleteView.as_view(), name='shelf_delete'),

]