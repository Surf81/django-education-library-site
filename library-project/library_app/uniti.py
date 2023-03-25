
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
