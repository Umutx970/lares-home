from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path('', views.home, name='home'),

    # AUTH
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # PRODUCTS
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # CART
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('increase-cart/<int:id>/', views.increase_cart, name='increase_cart'),
    path('decrease-cart/<int:id>/', views.decrease_cart, name='decrease_cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),

    # CHECKOUT
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),

    # ORDERS
    path('my-orders/', views.my_orders, name='my_orders'),

    # REVIEWS
    path('add-review/<int:id>/', views.add_review, name='add_review'),

    # FAVORITES
    path('toggle-favorite/<int:id>/', views.toggle_favorite, name='toggle_favorite'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-product/', views.add_product, name='add_product'),

    # CONTACT
    path('contact/', views.contact, name='contact'),
]