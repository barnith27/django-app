from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Product, Order
from .utils import add_two_numbers
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result =  add_two_numbers(2, 5)
        self.assertEqual(result, 7)

class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='drake_test', password='qwerty')

        content_type = ContentType.objects.get_for_model(Order)
        permission = Permission.objects.get(
            codename='view_order',
            content_type=content_type,
        )
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.order = Order.objects.create(delivery_address='kurgan 123',promocode='promo20',
                                          user=self.user)

    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse("shopapp:order_details", kwargs={'pk': self.order.pk}), HTTP_USER_AGENT='TestClient/1.0')
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertContains(response, self.order.user)


class OrdersExportTestCase(TestCase):
    fixtures = [
        'user-fixture.json',
        'product-fixture.json',
        'order',
    ]
    @classmethod
    def setUpClass(cls):
        cls.staff_user = User.objects.create_user(
            username='staff_user',
            password='qwerty',
            is_staff=True
        )

    @classmethod
    def tearDownClass(cls):
        cls.staff_user.delete()

    def setUp(self):
        self.client.force_login(self.staff_user)

    def test_order_export(self):
        print("Users:", User.objects.count())
        print("Products:", Product.objects.count())
        print("Order:", Order.objects.count())