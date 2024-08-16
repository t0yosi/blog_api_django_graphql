import django_filters
from .models import Author, Post, Comment


class AuthorFilter(django_filters.FilterSet):
    class Meta:
        model = Author
        fields = {
            "name": ["icontains"],
            "email": ["exact"],
        }

class PostFilter(django_filters.FilterSet):
    title_icontains = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains"
    )
    content_icontains = django_filters.CharFilter(
        field_name="content", lookup_expr="icontains"
    )
    author_name_exact = django_filters.CharFilter(
        field_name="author__name", lookup_expr="exact"
    )
    created_at_date = django_filters.DateFilter(
        field_name="created_at", lookup_expr="date"
    )
    created_at_gte = django_filters.DateFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_at_lte = django_filters.DateFilter(
        field_name="created_at", lookup_expr="lte"
    )


class CommentFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = {
            "content": ["icontains"],
            "post__title": ["icontains"],
            "created_at": ["date", "gte", "lte"],
        }
