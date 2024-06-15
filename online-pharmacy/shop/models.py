from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=20)
    category = models.CharField(max_length=20, default="")
    subcategory = models.CharField(max_length=20, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=1000)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="shop/images/default.jpg")
    available_pharmacies = models.ManyToManyField(User, related_name='available_products', blank=True)

    def __str__(self):
        return self.product_name


class UserProfile(models.Model):
    USER_ROLES = [
        ('Customer', 'Customer'),
        ('Pharmacist', 'Pharmacist'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=USER_ROLES, default='Customer')
    image = models.ImageField(upload_to='profile_pics/', default='')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    area = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    def get_area(self):
        return self.area
