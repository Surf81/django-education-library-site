from django.contrib import admin

from library_app.models import BookCoverModel, BookModel, BookSizeModel

# Register your models here.

@admin.register(BookModel)
class BookModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(BookCoverModel)
admin.site.register(BookSizeModel)