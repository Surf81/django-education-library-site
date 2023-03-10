from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class BookModel(models.Model):
    title = models.CharField("название", max_length=100, null=False, blank=False)
    description = models.TextField("описание")
    price = models.FloatField("цена", null=False, blank=False, validators=[MinValueValidator(0),])
    pages = models.IntegerField("количество страниц", validators=[MinValueValidator(0),])
    cover = models.ForeignKey("BookCoverModel", verbose_name="переплет", null=True, on_delete=models.SET_NULL)
    size = models.ForeignKey("BookSizeModel", verbose_name="размер", null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "book"
        verbose_name = "книга"
        verbose_name_plural = "книги"


class BookCoverModel(models.Model):
    cover = models.CharField("переплет", max_length=50, null=False, blank=False)

    class Meta:
        db_table = "cover"
        verbose_name = "переплет"
        verbose_name_plural = "виды переплета"


class BookSizeModel(models.Model):
    size = models.CharField("размер", max_length=50, null=False, blank=False)

    class Meta:
        db_table = "size"
        verbose_name = "размер"
        verbose_name_plural = "размеры"
