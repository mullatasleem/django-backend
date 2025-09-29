from django.urls import path, include
from rest_framework.routers import DefaultRouter
from website import views
from rest_framework.authtoken import views as drf_views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    # Products
    path('add_product/', views.add_product, name='add_product'),
    path('products_list/', views.products_list, name='products_list'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Users
    path('users_list/', views.users_list, name='users_list'),
    path('adduser/', views.add_user, name='add_user'),


    # Search & Product Detail
    path('search/', views.search, name='search'),
    path('product/<int:id>/', views.product_page, name='product_page'),

    # API
    path('token/', drf_views.obtain_auth_token, name='api_token_auth'),
    path('api/', include(router.urls)),
]
