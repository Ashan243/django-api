
from rest_framework.pagination import  LimitOffsetPagination

class DefaultPaginationClass(LimitOffsetPagination):
    page_size = 20
    limit_query_param = "type"
    offset_query_param = "billing"
    # www.localhost:8000/ecommerce/q?billing="monthly"&type="student"
    