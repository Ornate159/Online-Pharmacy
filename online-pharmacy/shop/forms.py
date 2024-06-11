from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Product
# shop/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileUpdateForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = UserProfile
        fields = ['image', 'full_name', 'address', 'gender', 'contact_number']

class CreateUserForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Pharmacist', 'Pharmacist'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']


class ProductForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('Prescribed Medicines', 'Prescribed Medicines'),
        ('OTC Medicines', 'OTC Medicines'),
        ('Healthcare Products', 'Healthcare Products'),
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta:
        model = Product
        fields = ['product_name', 'category', 'subcategory', 'price', 'desc', 'image']