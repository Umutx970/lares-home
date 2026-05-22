from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store.views import add_product, home, product_detail, add_to_cart, cart, checkout, increase_cart, decrease_cart, remove_from_cart
from store.views import home, product_detail, add_to_cart, cart, checkout, increase_cart, decrease_cart, remove_from_cart, order_success, my_orders, add_review, toggle_favorite, my_favorites, dashboard, contact
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('cart/increase/<int:id>/', increase_cart, name='increase_cart'),
    path('cart/decrease/<int:id>/', decrease_cart, name='decrease_cart'),
    path('cart/remove/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('order-success/', order_success, name='order_success'),
    path('accounts/', include('accounts.urls')),
    path('my-orders/', my_orders, name='my_orders'),
    path('add-review/<int:id>/', add_review, name='add_review'),
    path('favorite/<int:id>/', toggle_favorite, name='toggle_favorite'),
    path('favorites/', my_favorites, name='my_favorites'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add-product/', add_product, name='add_product'),
    path('contact/', contact, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)