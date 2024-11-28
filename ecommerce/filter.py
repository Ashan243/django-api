import django_filters
from models import Products


class ProductFilter(django_filters.FilterSet):
    
    # Custom field logic for querying
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    
    class Meta:
        model = Products
        fields = ["min_price", "max_price"]