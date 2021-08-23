from django.core.paginator import EmptyPage, Paginator
from django.http import Http404


class FoodgramPaginator(Paginator):

    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if number > 1 or number == 0:
                return self.num_pages
            else:
                raise Http404(f'Page with number {number} was not found')
