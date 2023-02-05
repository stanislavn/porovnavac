from django.contrib import admin

from .models import Category, Price, Product, Website

# Register your models here.


class PriceInline(admin.TabularInline):
    model = Price


class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInline]


admin.site.register(Category)
admin.site.register(Website)
admin.site.register(Product, ProductAdmin)
