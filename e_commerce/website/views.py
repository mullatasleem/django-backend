from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Products, AuthUser
from rest_framework import viewsets
from .serializers import ProductSerializer
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Sum, Avg, Count

# Home Page
@login_required
def home(request):
    product = Products.objects.first()
    content = {
        'title': "Welcome to our E-commerce.",
        'description': "Explore our products.",
        'products': Products.objects.all(),
        'product': product,
    }
    return render(request, 'website/index.html', content)


# Product Details
@login_required
def product_page(request, id):
    product = get_object_or_404(Products, id=id)
    return render(request, 'website/product_detail.html', {'product': product})


# Search Page
@login_required
def search(request):
    data = {
        'title': "Welcome to our E-commerce Search Page.",
        'description': "Search for your favourite products here.",
    }
    return render(request, 'website/index.html', data)


# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')
        return render(request, 'website/login.html', {"error": "Invalid username or password"})
    return render(request, 'website/login.html')


# Logout
@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')


# Signup
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if AuthUser.objects.filter(username=username).exists():
            return render(request, "website/signup.html", {"error": "Username already exists"})
        if AuthUser.objects.filter(email=email).exists():
            return render(request, "website/signup.html", {"error": "Email already exists"})

        user = AuthUser.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)
        return redirect("home")
    return render(request, "website/signup.html")


# Add Product
@login_required
def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        Products.objects.create(name=name, description=description, price=price, stock=stock)
        return redirect('products_list')
    return render(request, 'website/add_product.html')


# Products List
@login_required
def products_list(request):
    products = Products.objects.all()
    return render(request, 'website/products_list.html', {'products': products})


# Edit Product
@login_required
def edit_product(request, id):
    product = get_object_or_404(Products, id=id)
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.save()
        return redirect('products_list')
    return render(request, 'website/edit_product.html', {'product': product})


# Delete Product
@login_required
def delete_product(request, id):
    product = get_object_or_404(Products, id=id)
    product.delete()
    return redirect('products_list')

def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Save user with hashed password
        AuthUser.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        return redirect('users_list')  # redirect after adding user

    return render(request, 'website/add_user.html')

# Users List
@login_required
def users_list(request):
    users = AuthUser.objects.all()
    return render(request, 'website/users_list.html', {'users': users})


# API View - List Products
@login_required
def product_list(request):
    products = Products.objects.all().values('id', 'name', 'description', 'price', 'stock')
    return JsonResponse(list(products), safe=False)


# DRF Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer



def dashboard(request):
    # Aggregate product analysis
    total_products = Products.objects.count()
    total_stock = Products.objects.aggregate(Sum('stock'))['stock__sum'] or 0
    average_price = Products.objects.aggregate(Avg('price'))['price__avg'] or 0

    # Optionally, get price distribution for chart
    products = Products.objects.all()
    prices = [float(product.price) for product in products]

    context = {
        'total_products': total_products,
        'total_stock': total_stock,
        'average_price': average_price,
        'prices': prices,
    }
    return render(request, 'website/dashboard.html', context)