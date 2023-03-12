from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from pytils.translit import slugify


# Create your models here.
class BookModel(models.Model):
    title = models.CharField("название", max_length=100, null=False, blank=False)
    slug = models.SlugField("слаг", max_length=150, null=True, blank=False, unique=True)
    description = models.TextField("описание")
    price = models.FloatField(
        "цена",
        null=False,
        blank=False,
        validators=[
            MinValueValidator(0),
        ],
    )
    pages = models.IntegerField(
        "количество страниц",
        validators=[
            MinValueValidator(0),
        ],
    )
    publication_date = models.DateField(
        "дата публикации",
        null=False,
        blank=False,
    )
    cover = models.ForeignKey("BookCoverModel", verbose_name="переплет", null=True, on_delete=models.SET_NULL)
    size = models.ForeignKey("BookSizeModel", verbose_name="размер", null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "book"
        verbose_name = "книга"
        verbose_name_plural = "книги"
        get_latest_by = "publication_date"
        ordering = ["title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(BookModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("book-info-view", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class BookCoverModel(models.Model):
    cover = models.CharField("переплет", max_length=50, null=False, blank=False)

    class Meta:
        db_table = "cover"
        verbose_name = "переплет"
        verbose_name_plural = "виды переплета"

    def __str__(self):
        return self.cover


class BookSizeModel(models.Model):
    size = models.CharField("размер", max_length=50, null=False, blank=False)

    class Meta:
        db_table = "size"
        verbose_name = "размер"
        verbose_name_plural = "размеры"

    def __str__(self):
        return self.size
