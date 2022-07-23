from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Image, Category, Product, Response

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    fields = ['image_to_show', 'image', 'url']
    list_display = ['image_to_show']
    readonly_fields = ['image_to_show', 'url']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class ProductAdmin(SummernoteModelAdmin):
    list_display = ['name', 'category', 'price']
    summernote_fields = ['description']


class ResponseAdmin(admin.ModelAdmin):
    list_display = ["short_text", "product", "user"]


admin.site.register(Image, ImageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Response, ResponseAdmin)
