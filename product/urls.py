
from django.urls import path

from product import views as product_views

app_name = "product"
urlpatterns = [
    path(route="", view=product_views.product_list_view, name="product_list"),
    path(route="<slug>/", view=product_views.product_detail_view, name="product_detail"),
]
