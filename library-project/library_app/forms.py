from django.forms import DateInput, ModelChoiceField, NumberInput, Select, TextInput, Textarea
from django.forms import models

from library_app.models import BookCoverModel, BookModel, BookSizeModel


class BookForm(models.ModelForm):
    cover = ModelChoiceField(
        queryset=BookCoverModel.objects.all(),
        label="Обложка",
        empty_label="...выберите переплет...",
        widget=Select(attrs={"class": "form-control"}),
    )
    size = ModelChoiceField(
        queryset=BookSizeModel.objects.all(),
        label="Размер",
        empty_label="...выберите размер...",
        widget=Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = BookModel
        fields = ("title", "description", "publication_date", "price", "pages", "cover", "size")
        exclude = ("slug",)
        widgets = {
            "title": TextInput(attrs={"class": "form-control", "placeholder": "начните вводить..."}),
            "description": Textarea(attrs={"class": "form-control"}),
            "publication_date": DateInput(
                format="%d.%m.%Y", attrs={"placeholder": "ДД.ММ.ГГГГ", "class": "form-control"}
            ),
            "price": NumberInput(attrs={"class": "form-control"}),
            "pages": NumberInput(attrs={"class": "form-control"}),
        }
