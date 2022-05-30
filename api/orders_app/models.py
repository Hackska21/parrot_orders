from django.conf import settings
from django.db import models


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class Order(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    customer_name = models.CharField(max_length=250)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    created = models.DateTimeField(auto_now_add=True)

    products = models.ManyToManyField(
        'Product',
        through='OrderProducts'
    )


class Product(models.Model):
    name = NameField(primary_key=True, max_length=250)


class OrderProducts(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    order = models.ForeignKey('Order', on_delete=models.PROTECT)
    unit_price = models.DecimalField(decimal_places=2, max_digits=9)
    quantity = models.IntegerField()
