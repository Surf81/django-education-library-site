from django.urls import path
from .views import book_info_view, index_view, book_list_view, library_info_view

urlpatterns = [
    path('', index_view, name='index-view'),
    path('library/', book_list_view, name='book-list-view'),
    path('library/<slug:slug>', book_info_view, name='book-info-view'),
    path('about/', library_info_view, name='library-info-view'),
]
