# pagination.py
from typing import TypeVar, Generic, List
from mongoengine.queryset.queryset import QuerySet


T = TypeVar('T')


class Paginator(Generic[T]):
    def __init__(self, queryset: QuerySet, page: int, per_page: int):
        self.queryset = queryset
        self.page = page
        self.per_page = per_page

    def paginate(self) -> Pagination[T]:
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        items = self.queryset[start:end]
        total = self.queryset.count()

        return Pagination[T](

        )
