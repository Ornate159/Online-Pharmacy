from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("login/", views.Login, name="LogIn"),
    path("signup/", views.signup, name="SignUp"),
    path("logout/", views.Logout, name="Logout"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("search/", views.search, name="Search"),
    path("nomatch/", views.search, name="nomatch"),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path("checkout/", views.checkout, name="Checkout"),
    path("prescribed/", views.prescribed, name="prescribed"),
    path("otc/", views.otc, name="otc"),
    path("healthcare/", views.healthcare, name="healthcare"),
    path("pharmacist/", views.pharmacist, name="Pharmacist"),
    path("payment/", views.payment, name="payment"),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
]

urlpatterns += staticfiles_urlpatterns()
