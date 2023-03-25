from django.urls import path
from .views import *

urlpatterns = [
    # функции-представления
    path("", index_view, name="index-view"),  # начальная страница
    path("about/", library_info_view, name="library-info-view"),  # информация о библиотеке
    path("library/<slug:slug>", book_detail_view, name="book-detail-view"),  # информация о книге
    path("library/", book_list_view, name="book-list-view"),  # список книг
    path("library/addbook/", book_addnew, name="book-create"),
    path("library/editbook/<slug:slug>", book_edit, name="book-edit"),
    path("library/delbook/<slug:slug>", book_delete, name="book-delete"),
    # классы-представления
    path("about/classview", LibraryInfoView.as_view(), name="library-classview-info-view"),  # информация о библиотеке
    path("library/classview/<slug:slug>", BookDetailView.as_view(), name="book-classview-detail"),  # список книг
    path("library/classview/", BookListView.as_view(), name="book-classview"),  # список книг
    path("library/classview/addbook/", BookCreateView.as_view(), name="book-classview-create"),
    path("library/classview/editbook/<slug:slug>", BookEditView.as_view(), name="book-classview-edit"),
    path("library/classview/delbook/<slug:slug>", BookDeleteView.as_view(), name="book-classview-delete"),
]
