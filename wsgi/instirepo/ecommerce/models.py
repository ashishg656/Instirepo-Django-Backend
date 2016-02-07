from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    mrp = models.CharField(null=True, max_length=255)
    price = models.CharField(null=True, max_length=255)
    image1 = models.ImageField(upload_to='product_images', null=True, blank=True)
    image2 = models.ImageField(upload_to='product_images', null=True, blank=True)
    image3 = models.ImageField(upload_to='product_images', null=True, blank=True)
    image4 = models.ImageField(upload_to='product_images', null=True, blank=True)
    image5 = models.ImageField(upload_to='product_images', null=True, blank=True)
    image6 = models.ImageField(upload_to='product_images', null=True, blank=True)
    image7 = models.ImageField(upload_to='product_images', null=True, blank=True)
    image8 = models.ImageField(upload_to='product_images', null=True, blank=True)
    category = models.ForeignKey('ProductCategories', null=True)

    contact_number = models.CharField(max_length=255, null=True)

    stock = models.IntegerField(null=True)

    college = models.ForeignKey('instirepo_web.College', null=True)
    uploader = models.ForeignKey(User)

    is_old_product = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_cod_payment = models.BooleanField()
    is_online_payment = models.BooleanField()
    time = models.DateTimeField(auto_now=True)


class ProductCategories(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_categories_images', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)


class Orders(models.Model):
    CANCELLED = 'CANCELLED'
    IN_PROCESS = 'IN_PROCESS'
    SUCCESSFUL = 'SUCCESSFUL'
    RETURNED = 'RETURNED'
    IN_TRANSIT = 'IN_TRANSIT'

    TYPE_OF_VISIBILITY = (
        (CANCELLED, 'CANCELLED'),
        (IN_PROCESS, 'IN_PROCESS'),
        (SUCCESSFUL, 'SUCCESSFUL'),
        (RETURNED, 'RETURNED'),
        (IN_TRANSIT, 'IN_TRANSIT'),
    )

    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    amount = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    product_name = models.TextField(null=True)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(null=True)
    status = models.CharField(max_length=255, choices=TYPE_OF_VISIBILITY)


class ProductComments(models.Model):
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    is_active = models.BooleanField(default=True)


class ProductFavourites(models.Model):
    time = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    is_active = models.BooleanField(default=True)


class ProductViews(models.Model):
    time = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    is_active = models.BooleanField(default=True)


class RecentlyViewedProducts(models.Model):
    time = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product,related_name='recently_viewed')
    user = models.ForeignKey(User)
    is_active = models.BooleanField(default=True)
    def __unicode__(self):
        return str(self.product.name)
