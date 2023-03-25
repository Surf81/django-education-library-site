from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator

from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView

from .forms import BookForm
from .models import BookModel
from .uniti import PaginatorBySlag



#####################################################################
# использование функций-представлений

def index_view(request):
    """Домашняя страница"""
    return render(request, "library_app/index.html", {"title": "Библиотека"})


def book_list_view(request):
    """Список книг"""
    allbooks = BookModel.objects.all()
    paginator = Paginator(allbooks, 3)
    num_page = request.GET.get('page', 1)
    page = paginator.get_page(num_page)
    context = {
        "title": "Каталог книг",
        "books": page.object_list,
        "paginator": paginator,
        "is_paginated": True,
        "page_obj": page,
        "start_page_number": page.start_index()-1
    }
    return render(request, "library_app/book_catalog.html", context)


def book_detail_view(request, slug=None):
    """Информация о книге"""
    book = get_object_or_404(BookModel, slug=slug)
    # print(BookModel.objects.earliest())
    # print(BookModel.objects.latest())
    # next_book = book.get_next_by_publication_date()
    # previous_book = book.get_previous_by_publication_date()
    paginator = PaginatorBySlag(BookModel.objects.all(), book)

    context = {
        "title": book.title,
        "book": book,
        "paginator": paginator,
        "fields": ["title", "description", "publication_date", "pages", "size", "cover", "price"],
    }
    return render(request, "library_app/book_detail.html", context)


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


def book_addnew(request):
    """Добавление новой книги"""
    if request.method == 'GET':
        bookform = BookForm()
        context = {
            'form': bookform,
            'title': 'Добавление записи'
        }
        return render(request, "library_app/book_addnew.html", context)
    elif request.method == 'POST':
        bookform = BookForm(request.POST)
        if bookform.is_valid():
            bookform.save()
            return HttpResponseRedirect(reverse('book-list-view'))
        else:
            context = {
                'form': bookform,
                'title': 'Корректировка записи'
            }
            return render(request, "library_app/book_addnew.html", context)


def book_edit(request, slug):
    """Редактирование записи о книге"""
    book = BookModel.objects.get(slug=slug)
    if request.method == 'GET':
        bookform = BookForm(instance=book)
        context = {
            'form': bookform,
            'title': 'Редактирование записи'
        }
        return render(request, "library_app/book_edit.html", context)
    elif request.method == 'POST':
        bookform = BookForm(request.POST, instance=book)
        if bookform.is_valid():
            bookform.save()
            return HttpResponseRedirect(reverse('book-list-view'))
        else:
            context = {
                'form': bookform,
                'title': 'Корректировка записи'
            }
            return render(request, "library_app/book_edit.html", context)


def book_delete(request, slug):
    """Удаление записи о книге"""
    book = BookModel.objects.get(slug=slug)
    if request.method == 'GET':
        context = {
            'object': book,
            'title': 'Удаление записи'
        }
        return render(request, "library_app/book_confirm_delete.html", context)
    elif request.method == 'POST':
        book.delete()
        return HttpResponseRedirect(reverse('book-list-view'))



#######################################################################
# Использование классов-представлений

class BookListView(ListView):
    extra_context = {
        'title': 'Каталог книг'
    }
    model = BookModel
    template_name = "library_app/book_catalog.html"
    context_object_name = "books"
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["start_page_number"] = context['page_obj'].start_index()-1
        return context


class BookDetailView(DetailView):
    extra_context = {
        "fields": ["title", "description", "publication_date", "pages", "size", "cover", "price"],
    }
    model = BookModel
    template_name = "library_app/book_detail.html"
    context_object_name = "book"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = context['book'].title
        context['paginator'] = PaginatorBySlag(BookModel.objects.all(), context['book'])
        return context


class BookCreateView(CreateView):
    extra_context = {
        'title': 'Добавление записи'
    }
    template_name = "library_app/book_addnew.html"
    form_class = BookForm
    success_url = reverse_lazy('book-list-view')
    
class BookEditView(UpdateView):
    extra_context = {
        'title': 'Изменение записи'
    }
    model = BookModel
    template_name = "library_app/book_edit.html"
    form_class = BookForm
    success_url = reverse_lazy('book-list-view')

class BookDeleteView(DeleteView):
    extra_context = {
        'title': 'Удаление записи'
    }
    model = BookModel
    template_name = "library_app/book_confirm_delete.html"
    success_url = reverse_lazy('book-list-view')


class LibraryInfoView(TemplateView):
    totalprice = BookModel.objects.aggregate(Sum("price"))["price__sum"]
    countbook = BookModel.objects.count()
    extra_context = {
        "title": "Информация о бибилиотеке",
        "countbook": countbook,
        "totalprice": totalprice,
    }
    template_name = "library_app/library_info.html"