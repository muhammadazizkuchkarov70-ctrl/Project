from django import template

from store.models import Category, FavoriteProduct


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter(parent=None)


@register.simple_tag()
def get_favorite_products(user):
    fav_pr_objects = FavoriteProduct.objects.filter(user=user)
    user_fav_products = []
    for obj in fav_pr_objects:
        user_fav_products.append(obj.product)
    return user_fav_products