from django.contrib import admin

from library_app.models import BookCoverModel, BookModel, BookSizeModel

# Register your models here.

@admin.register(BookModel)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ("title", "size", "cover", "price")
    list_display_links = ("title", "size", "cover")
    prepopulated_fields = {"slug": ("title",)}
    empty_value_display="не выбрано"
    list_editable = ("price",)
    list_filter = ("size", "cover")
    radio_fields = {"size": admin.VERTICAL}
    search_fields = ("title",)


admin.site.register(BookCoverModel)
admin.site.register(BookSizeModel)