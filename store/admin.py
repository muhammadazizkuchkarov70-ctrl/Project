from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

from .models import *


class PhotoInline(admin.TabularInline):
    fk_name = 'product'
    model = Photo
    extra = 3

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_count_products')
    prepopulated_fields = {'slug': ('title',)}

    def get_count_products(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_count_products.short_description = 'Количесто товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('pk', 'title', 'category', 'color', 'material', 'size',
                    'price', 'created_at', 'quantity', 'company',
                    'get_first_photo')
    list_display_links = ('title', )
    list_filter = ('category', 'company', 'size', 'color', 'material', 'price')
    inlines = [PhotoInline]
    list_editable = ('price',)

    def get_first_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f"<img src='{obj.images.all()[0].image.url}' width='50'>")
            except:
                return '-'
        else:
            return '-'

    get_first_photo.short_description = 'Миниатюра'

admin.site.register(Company)
admin.site.register(Photo)
admin.site.register(Profile)

admin.site.register(Review)
admin.site.register(Mail)
admin.site.register(FavoriteProduct)
