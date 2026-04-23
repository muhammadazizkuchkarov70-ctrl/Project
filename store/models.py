from django.contrib.auth.models import User
from django.db import models

from django.urls import reverse


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=150,
                             verbose_name='Наименование категории')

    image = models.ImageField(upload_to='categories/',
                              null=True, blank=True,
                              verbose_name='Изображение категории')
    # Название категории для подставки в ссылку
    slug = models.SlugField(unique=True, null=True)

    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True, blank=True,
                               verbose_name='Родитель',
                               related_name='subcategories')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_page', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Company(models.Model):
    title = models.CharField(max_length=150,
                             verbose_name='Наименование компании')
    description = models.TextField(verbose_name='Описание компании')
    image = models.ImageField(upload_to='companies/',
                              verbose_name='Изображение',
                              blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование продукта')
    description = models.TextField(default='Здесь скоро будет описание',
                                   verbose_name='Описание продукта')
    price = models.FloatField(verbose_name='Цена продукта')
    color = models.CharField(max_length=150, default='Серебрянный',
                             verbose_name='Цвет продукта')
    material = models.CharField(max_length=150, default='Серебро',
                                verbose_name='Материал продукта')
    size = models.IntegerField(default=40, verbose_name='Размер продукта')
    quantity = models.IntegerField(default=0, verbose_name='Количество на складе')

    company = models.ForeignKey(Company, on_delete=models.CASCADE,
                                verbose_name='Компания продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Категория продукта',
                                 related_name='products')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания продукта')
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.title

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.all()[0].image.url
            except:
                return '-'
        else:
            return '-'

    def get_absolute_url(self):
        return reverse('product_page', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Photo(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Продукт',
                                related_name='images')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class Profile(models.Model):
    avatar = models.ImageField(upload_to='photos/users/',
                               verbose_name='Аватар пользователя',
                               blank=True, null=True)
    phone = models.CharField(max_length=255,
                             verbose_name='Номер телефона',
                             default='+12345678900')
    bio = models.CharField(max_length=255,
                           verbose_name='О себе',
                           default='Коротко о себе ...')
    city = models.CharField(max_length=255,
                            verbose_name='Город',
                            default='City ...')
    region = models.CharField(max_length=255,
                              verbose_name='Штат/Регион',
                              default='State/Region ...')
    job = models.CharField(max_length=255,
                           verbose_name='Профессия',
                           default='Unemployed ...')
    instagram = models.CharField(max_length=255,
                                 verbose_name='Инстаграм',
                                 default='@username')
    telegram = models.CharField(max_length=255,
                                verbose_name='Телеграм',
                                default='@username')
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='Пользователь')

    def str(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Review(models.Model):
    text = models.TextField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Избранный продукт'
        verbose_name_plural = 'Избранные продукты'


class Mail(models.Model):
    mail = models.EmailField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name = 'Почта'
        verbose_name_plural = 'Почты'


class Customer(models.Model):
    user = models.OneToOneField(User, models.SET_NULL,
                                blank=True, null=True)
    first_name = models.CharField(max_length=255,
                                  default='',
                                  verbose_name='Имя клиента')
    last_name = models.CharField(max_length=255,
                                 default='',
                                 verbose_name='Фамилия клиента')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    shipping = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} ---> {self.pk}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_cart_final_price(self):
        order_products = self.orderproduct_set.all()
        final_price = sum([product.get_total_price for product in order_products])
        return final_price
        # Мы захватываем все объекты созданные на основе класса OrderProduct которые принадлежат к заказу
        # Генерируем список


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,
                              blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                blank=True, null=True)

    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товар в заказе'

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'


