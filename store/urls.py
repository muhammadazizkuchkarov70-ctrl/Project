from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('store/category/<slug:slug>/', category_page, name='category_page'),
    path('product/<slug:slug>/', product_page, name='product_page'),

    path('login/', login_user, name='login_user'),
    path('registration/', registration_user, name='registration_user'),
    path('logout/', logout_user, name='logout_user'),

    path('save_review/<int:product_id>/', save_review, name='save_review'),

    path('search_page/', search_page_view, name='search_page'),
    path('search_results/', search_results, name='search_results'),

    path('save_mail/', save_mail, name='save_mail'),
    path('send_mail/', send_mail_to_customers, name='send_mail'),

    path('add_favorite/<slug:product_slug>/', add_favorite_products, name="add_favorite"),
    path('fav_products/', favorite_products, name='favorite_products'),

    path('cart/', cart, name="cart"),
    path('to_cart/<int:product_id>/<str:action>/', to_cart, name="to_cart"),
    path('checkout/', checkout, name="checkout"),

    path('payment/', create_payment_session, name='payment'),
    path('payment_success/', successPayment, name='success'),
    path('account/', account, name='account'),

]