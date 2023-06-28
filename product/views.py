from django.shortcuts import render
from django.views import generic

from product.models import Product


class ProductListView(generic.ListView):
    paginate_by = 12
    queryset = Product.objects.filter(published=True)
    context_object_name = "product_list"
    template_name = "product/product_list.html"


product_list_view = ProductListView.as_view(extra_context={"page_title": "Nos produits"})


class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = "product"
    template_name = "product/product_detail.html"

    def get_context_data(self, **kwargs):
        kwargs["page_title"] = self.object.title
        return super().get_context_data(**kwargs)


product_detail_view = ProductDetailView.as_view()
