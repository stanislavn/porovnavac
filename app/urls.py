from django.urls import path

from app.views import ProductDetailView

from . import views

app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("produkt/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("celery", views.add, name="add"),
]
