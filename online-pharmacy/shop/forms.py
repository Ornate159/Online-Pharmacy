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

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['image', 'full_name', 'address', 'area', 'contact_number']

class CreateUserForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Pharmacist', 'Pharmacist'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    image = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'image']


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