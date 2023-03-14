from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Min

from library_app.models import BookModel


def index_view(request):
    """Домашняя страница"""
    return render(request, "library_app/index.html", {"title": "Библиотека"})


def book_list_view(request):
    """Список книг"""
    allbooks = BookModel.objects.all()
    context = {
        "title": "Каталог книг",
        "books": allbooks,
    }
    return render(request, "library_app/book_catalog.html", context)


class PaginatorBySlag:
    """Вспомогательный класс для пагинации между записями книг
    """
    def __init__(self, object_list, current_page):
        self.object_list = object_list
        self.current_page = current_page
        self.has_previous = False
        self.has_next = False
        try_find = True
        for page in self.object_list:
            if try_find and page.slug != self.current_page.slug:
                self.previous_page = page
                self.has_previous = True
            if not try_find:
                self.next_page = page
                self.has_next = True
                break
            if page.slug == self.current_page.slug:
                try_find = False


def book_info_view(request, slug=None):
    """Информация о книге"""
    book = get_object_or_404(BookModel, slug=slug)
    # print(BookModel.objects.earliest())
    # print(BookModel.objects.latest())
    # next_book = book.get_next_by_publication_date()
    # previous_book = book.get_previous_by_publication_date()
    paginator = PaginatorBySlag(BookModel.objects.all(), book)

    context = {
        "title": book.title,
        "paginator": paginator,
        "fields": ["title", "description", "publication_date", "pages", "size", "cover", "price"],
    }
    return render(request, "library_app/book_info.html", context)


def library_info_view(request):
    """Информация о книгах в библиотеке"""
    totalprice = BookModel.objects.aggregate(Sum("price"))["price__sum"]
    countbook = BookModel.objects.count()
    context = {
        "title": "Информация о бибилиотеке",
        "countbook": countbook,
        "totalprice": totalprice,
    }
    return render(request, "library_app/library_info.html", context)
