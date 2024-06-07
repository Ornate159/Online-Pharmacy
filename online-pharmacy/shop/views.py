from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, UserProfile
from django.contrib import messages
from math import ceil
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, ProductForm
from .models import Product, UserProfile
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import date

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

from django.shortcuts import redirect

def Login(request):
    if request.user.is_authenticated:
        return redirect('/shop')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/shop')
            else:
                messages.info(request, 'Wrong Username or Password')

        context = {}
        return render(request, 'shop/login.html', context)

def signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            UserProfile.objects.create(user=user, role=role)
            messages.success(request, 'Your Account Has Been Created')
            return redirect('/shop/login')
    context = {'form': form}
    return render(request, 'shop/signup.html', context)

@login_required
def index(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        role = user_profile.role
    except ObjectDoesNotExist:
        # Handle the case where the user profile doesn't exist
        role = None
    
    # Your existing code
    products = Product.objects.all()
    listAll = []
    listCat = Product.objects.values('category', 'id')
    allCat = {item['category'] for item in listCat}
    for cat in allCat:
        item = Product.objects.filter(category=cat)
        x = len(products)
        slideN = x // 4 + ceil((x / 4 - (x // 4)))
        listAll.append([item, range(1, slideN), slideN])

    context = {'listAll': listAll, 'role': role}
    return render(request, 'shop/index.html', context)

def Logout(request):
    logout(request)
    return redirect('/shop/login')

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/contact.html')

def search(request):
    products = Product.objects.all()
    keyword = request.GET.get('search')
    listAll = []
    listCat = Product.objects.values('category', 'id')
    allCat = {item['category'] for item in listCat}
    for cat in allCat:
        list = Product.objects.filter(category=cat)
        result = [item for item in list if len(keyword) >= 3 and keyword in item.product_name.lower() or keyword in item.category.lower() or keyword in item.subcategory.lower()]

        x = len(products)
        slideN = x // 4 + ceil((x / 4 - (x // 4)))
        all = {'listAll': listAll}
        listAll.append([result, range(1, slideN), slideN])
    if len(listAll) == 0:
        return render(request, 'shop/nomatch.html')
    else:
        return render(request, 'shop/search.html', all)

def product(request, id):
    product = Product.objects.filter(id=id)
    return render(request, 'shop/product.html', {'product': product[0]})

def checkout(request):
    return render(request, 'shop/checkout.html')

def prescribed(request):
    products = Product.objects.all()
    listAll = []
    listCat = Product.objects.values('category', 'id')
    allCat = {item['category'] for item in listCat}
    for cat in allCat:
        item = Product.objects.filter(category='Prescribed Medicines')
        x = len(products)
        slideN = x // 4 + ceil((x / 4 - (x // 4)))

    all = {'listAll': listAll}
    listAll.append([item, range(1, slideN), slideN])
    return render(request, 'shop/prescribed.html', all)

def otc(request):
    products = Product.objects.all()
    listAll = []
    listCat = Product.objects.values('category', 'id')
    allCat = {item['category'] for item in listCat}
    for cat in allCat:
        item = Product.objects.filter(category='OTC Medicines')
        x = len(products)
        slideN = x // 4 + ceil((x / 4 - (x // 4)))

    all = {'listAll': listAll}
    listAll.append([item, range(1, slideN), slideN])
    return render(request, 'shop/prescribed.html', all)

def healthcare(request):
    products = Product.objects.all()
    listAll = []
    listCat = Product.objects.values('category', 'id')
    allCat = {item['category'] for item in listCat}
    for cat in allCat:
        item = Product.objects.filter(category='Healthcare Products')
        x = len(products)
        slideN = x // 4 + ceil((x / 4 - (x // 4)))

    all = {'listAll': listAll}
    listAll.append([item, range(1, slideN), slideN])
    return render(request, 'shop/prescribed.html', all)

def pharmacist(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.pub_date = date.today()  # Set the publication date to today
            product.save()
            messages.success(request, 'Product has been added successfully.')
            return redirect('/shop/pharmacist')
    else:
        form = ProductForm()
    return render(request, 'shop/pharmacist.html', {'form': form})