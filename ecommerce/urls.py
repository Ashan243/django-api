from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from .views import (
    UserViewSet,
    address_detail,
    ProductViewSet,
    CategoryViewSet,
    ReviewViewSet
)
from pprint import pprint
# Map request handling function to the endpoint
# Class to this is called URLPattern
# urlpatterns

#<int:pk>
# Nested Routing

new_router = routers.DefaultRouter()
new_router.register("products", ProductViewSet)
new_router.register("category", CategoryViewSet)
# *args

new_nested_router_products = routers.NestedDefaultRouter(new_router, "products", lookup="product_pk")
new_nested_router_products.register("reviews", ReviewViewSet, basename="product-reviews")
# htto://localhost:8000/products/1/reviews/2
pprint(new_nested_router_products.urls)
pprint(new_router.urls)

new_nested_router_category = routers.NestedDefaultRouter(new_router, "category", lookup="category_pk")



urlpatterns = [
    path("", include(new_router.urls)),
    path("", include(new_nested_router_products.urls))
]
    # path("", include(default_router.urls), name="address_details"), #
    # path("users/<int:pk>", address_detail, name="address_detail"), #0,1
    # # path("", include(product_router.urls)),
    # path(r"", include(nested_router.urls), name="review_details" )
    # name contains details ---> retreive()
    # name contains list ====> list()

    
    


