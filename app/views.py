from django.db.models import Avg
# Create your views here.
from django.http import HttpResponse
from django.views.generic.detail import DetailView

from .models import Price, Product
from .tasks import add_to_db


def add(request):
    result = add_to_db.delay()
    return HttpResponse("celery prebehlo")


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["high"] = (
            Price.objects.filter(product_id=self.get_object()).order_by("price").last()
        )
        context["low"] = (
            Price.objects.filter(product_id=self.get_object()).order_by("-price").last()
        )
        context["avg"] = Price.objects.filter(product_id=self.get_object()).aggregate(
            avg_price=Avg("price")
        )
        print(context)
        return context
