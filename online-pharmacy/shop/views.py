from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, UserProfile
from django.contrib import messages
from math import ceil
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, ProductForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, UserProfileUpdateForm

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        try:
            profile_instance = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile_instance = None
        
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile_instance)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            if p_form:
                profile = p_form.save(commit=False)
                profile.user = request.user
                profile.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        try:
            profile_instance = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile_instance = None

        p_form = UserProfileUpdateForm(instance=profile_instance)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'shop/profile.html', context)




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

def index(request):
    role = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            role = user_profile.role
        except ObjectDoesNotExist:
            pass
    
    products = Product.objects.all()
    listAll = []
    listCat = Product.objects.values('category', 'id')
    allCat = {item['category'] for item in listCat}
    for cat in allCat:
        item = Product.objects.filter(category=cat)
        x = len(products)
        slideN = x // 4 + ceil((x / 4 - (x // 4)))
        listAll.append([item, range(1, slideN), slideN])

    context = {'listAll': listAll, 'role': role, 'is_authenticated': request.user.is_authenticated}
    return render(request, 'shop/index.html', context)

def Logout(request):
    logout(request)
    return redirect('/shop/login')

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/contact.html')

def payment(request):
    return render(request, 'shop/payment.html')

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

def checkout(request):
    return render(request, 'shop/checkout.html')

def otc(request):
    products = Product.objects.filter(category='OTC Medicines')
    context = {'products': products}
    return render(request, 'shop/otc.html', context)

def prescribed(request):
    products = Product.objects.filter(category='Prescribed Medicines')
    context = {'products': products}
    return render(request, 'shop/prescribed.html', context)

def healthcare(request):
    products = Product.objects.filter(category='Healthcare Products')
    context = {'products': products}
    return render(request, 'shop/healthcare.html', context)

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

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product.html', {'product': product})
