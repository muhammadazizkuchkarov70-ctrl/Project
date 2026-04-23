import stripe
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required   # ← ЭТО СЮДА
from django.contrib.auth import authenticate, login, logout
from .models import *

from shop import settings
# Create your views here.
from .models import *
from .forms import *
from .utils import *


def index(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'store/index.html', context)


def category_page(request, slug):
    main_category = Category.objects.get(slug=slug)
    subcategories = main_category.subcategories.all()
    products = Product.objects.filter(category__in=subcategories)

    colors = []
    materials = []

    for product in products:
        lst_colors = product.color.split(', ')
        colors += [color.title() for color in lst_colors if color.title() not in colors]
        # for color in lst_colors:
        #     if color.title() not in colors:
        #         colors.append(color.title())
        lst_materials = product.material.split(', ')
        materials += [material.title() for material in lst_materials if material.title() not in materials]
        # for material in lst_materials:
        #     if material.title() not in materials:
        #         materials.append(material.title())

    context = {
        'products': products,
        'title': f'Категория: {main_category.title}',
        'colors': colors,
        'materials': materials,
        'subcategories': subcategories,
        'main_category': main_category
    }

    color_field = request.GET.get('color')
    if color_field:
        context['products'] = Product.objects.filter(
            color__iregex=color_field
        )
        context['header_c'] = color_field

    material_field = request.GET.get('material')
    if material_field:
        context['products'] = Product.objects.filter(
            material__iregex=material_field
        )
        context['header_m'] = f"{material_field}"

    sort_field = request.GET.get('sort')
    if sort_field:
        if sort_field == 'new':
            context['products'] = Product.objects.all().order_by('-created_at')
            context['header_s'] = "Что нового !"
        elif sort_field == 'max_min':
            context['products'] = Product.objects.all().order_by('-price')
            context['header_s'] = "Цена по убыванию !"
        elif sort_field == 'min_max':
            context['products'] = Product.objects.all().order_by('price')
            context['header_s'] = "Цена по возрастанию !"

    subcategory_field = request.GET.get('subcategory')
    if subcategory_field:
        subcategory = Category.objects.get(title=subcategory_field)
        context['products'] = Product.objects.filter(category=subcategory.pk)
        context['header_sub'] = f"{subcategory_field}"

    return render(request, 'store/category_detail.html', context)


def product_page(request, slug):
    product = Product.objects.get(slug=slug)

    products = Product.objects.all()
    import random
    rec = random.choices(products, k=4)

    reviews = Review.objects.filter(product=product)

    context = {
        'title': product.title,
        'product': product,
        'rec': rec,
        'reviews': reviews
    }
    if request.user.is_authenticated:
        context['review_form'] = ReviewForm()
    return render(request, 'store/product_detail.html', context)


def registration_user(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            # success message
            return redirect('login_user')
        else:
            # error message
            return redirect('registration_user')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
        'title': 'Регистрация пользователя'
    }
    return render(request, 'store/registration.html', context)


def login_user(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                # success message
                return redirect('index')
            else:
                # error message
                return redirect('login_user')
        else:
            # error message
            return redirect('login_user')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'title': 'Вход в аккаунт'
    }

    return render(request, 'store/login.html', context)


def logout_user(request):
    logout(request)
    # success message
    return redirect('index')


def save_review(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        review.product = product
        review.save()

        # success message
        return redirect('product_page', product.slug)
    else:
        # error message
        return redirect('product_page', product.slug)


def search_page_view(request):
    products = Product.objects.all()
    context = {
        'title': "Поиск",
        'products': products
    }
    return render(request, "store/search_page.html", context)


def search_results(request):
    word = request.GET.get('q')
    try:
        company = Company.objects.get(title__iregex=word.capitalize())
        products = Product.objects.filter(
            Q(title__iregex=word) | Q(description__iregex=word) | Q(company=company)
        )
    except:
        products = Product.objects.filter(
            Q(title__iregex=word) | Q(description__iregex=word)
        )

    context = {
        'title': 'Результаты поиска',
        'products': products
    }

    return render(request, "store/search_page.html", context)


def save_mail(request):
    email = request.POST.get('email')
    user = request.user if request.user.is_authenticated else None

    if user:
        Mail.objects.create(user=user, mail=email)
        page = request.META.get('HTTP_REFERER')
        # success message
        return redirect(page)
    else:
        # error message
        return redirect('login_user')


@user_passes_test(lambda u: u.is_superuser)
def send_mail_to_customers(request):
    from shop import settings
    if request.user.is_superuser and request.method == "POST":
        subject = request.POST.get('subject')
        text = request.POST.get('text')
        mail_list = Mail.objects.all()
        for email in mail_list:
            send_mail(
                subject=subject,
                message=text,
                from_email=settings.EMAIL_HOST_PASSWORD,
                recipient_list=[email],
                fail_silently=True
            )
            # success message
            return redirect('index')

    return render(request, 'store/send_mail.html')


def add_favorite_products(request, product_slug):
    user = request.user if request.user.is_authenticated else None
    product = Product.objects.get(slug=product_slug)
    fav_pr_objects = FavoriteProduct.objects.filter(user=user)
    user_fav_products = []
    for obj in fav_pr_objects:
        user_fav_products.append(obj.product)

    if user:
        if product in user_fav_products:
            fav_product = FavoriteProduct.objects.get(user=user, product=product)
            fav_product.delete()
            next_page = request.META.get('HTTP_REFERER')
            # message red
            return redirect(next_page)
        else:
            FavoriteProduct.objects.create(
                user=user, product=product
            )
            next_page = request.META.get('HTTP_REFERER')
            # message green
            return redirect(next_page)
    else:
        return redirect('login_user')


def favorite_products(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        fav_pr_objects = FavoriteProduct.objects.filter(user=user)
        user_fav_products = []
        for obj in fav_pr_objects:
            user_fav_products.append(obj.product)

    context = {
        'title': "Избранные товары",
        'products': user_fav_products
    }

    return render(request, "store/fav_products.html", context)


def cart(request):
    cart_info = get_cart_data(request)
    context = {
        "title": "Ваша корзина",
        'order': cart_info['order'],
        'products': cart_info['products'],
        'cart_total_price': cart_info['cart_total_price'],
    }

    return render(request, "store/cart.html", context)


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        CartForAuthenticatedUser(request, product_id, action)
        return redirect('cart')
    else:
        # error message
        return redirect('login_user')


def checkout(request):
    cart_info = get_cart_data(request)
    context = {
        "customer_form": CustomerForm(),
        "shipping_form": ShippingForm(),
        "title": "Оформление заказа",
        'order': cart_info['order'],
        'products': cart_info['products'],
        'cart_total_price': cart_info['cart_total_price'],
    }
    return render(request, "store/checkout.html", context)


def create_payment_session(request):
    if request.method == "POST":
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
        total_price = cart_info['cart_total_price']
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Продукт TOTEMBO'
                    },
                    'unit_amount': int(total_price * 100)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("success"))
        )
        return redirect(session.url, 303)


def successPayment(request):
    user_cart = CartForAuthenticatedUser(request)
    user_cart.clear()
    return render(request, 'store/success.html')

@login_required
def account(request):
    return render(request, 'account.html')