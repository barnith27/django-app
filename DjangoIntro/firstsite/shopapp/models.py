from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Product(models.Model):
    class Meta:
        ordering = ["name", "price"]

    name = models.CharField(max_length= 100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    def __str__(self)-> str:
        return f'Product(pk= {self.pk}, name= {self.name!r})'

class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")

