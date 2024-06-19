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
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomPasswordChangeForm

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        if request.user.is_authenticated:
            if 'available' in request.POST:
                if request.user not in product.available_pharmacies.all():
                    product.available_pharmacies.add(request.user)
                    messages.success(request, 'Product marked as available.')
                else:
                    messages.info(request, 'You are already marked as available for this product.')
            elif 'not_available' in request.POST:
                if request.user in product.available_pharmacies.all():
                    product.available_pharmacies.remove(request.user)
                    messages.success(request, 'Product marked as not available.')
                else:
                    messages.info(request, 'You are already marked as not available for this product.')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'You need to be logged in to perform this action.')

    available_pharmacies = product.available_pharmacies.all()

    print(available_pharmacies)

    pharmacies_with_area = [
        {
            "pharmacy": pharmacy,
            "area": pharmacy.userprofile.area if hasattr(pharmacy, 'userprofile') else "N/A"
        }
        for pharmacy in available_pharmacies
    ]

    context = {
        'product': product,
        'available_pharmacies': available_pharmacies,
        'pharmacies_with_area': pharmacies_with_area,
        'user_role': request.user.userprofile.role if request.user.is_authenticated else None,
    }

    return render(request, 'shop/product.html', context)

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
            return redirect('/shop/profile_view')
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


@login_required
def profile_view(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'shop/profile_view.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/shop/profile') 
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'shop/change_password.html', {'form': form})


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
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            image = form.cleaned_data.get('image')
            UserProfile.objects.create(user=user, role=role, image=image)
            messages.success(request, 'Your Account Has Been Created')
            return redirect('/shop/login')
    else:
        form = CreateUserForm()
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

def help(request):
    return render(request, 'shop/help.html')

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
        result = [item for item in list if len(keyword) >= 1 and keyword.lower() in item.product_name.lower()]

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
