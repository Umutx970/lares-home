from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, Category, Order, OrderItem, Review, Favorite


def home(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')

    products = Product.objects.filter(is_active=True, price__gte=100)

    if category_id:
        products = products.filter(category_id=category_id)

    if search_query:
        products = products.filter(name__icontains=search_query)

    categories = Category.objects.all()
    reviews = Review.objects.select_related('user', 'product').filter(rating__gte=4).order_by('-id')[:3]

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
        'reviews': reviews,
        'cart_count': cart_count,
        'search_query': search_query,
        'selected_category': category_id,
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id, is_active=True)
    average_rating = product.reviews.aggregate(avg=Avg('rating'))['avg']

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request, 'store/product_detail.html', {
        'product': product,
        'cart_count': cart_count,
        'average_rating': average_rating,
    })


def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart[product_id] = cart.get(product_id, 0) + quantity
    request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            total_price=total,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price,
            )

        order_products_text = ""
        for item in cart_items:
            order_products_text += f"- {item['product'].name} x {item['quantity']} = ₺{item['subtotal']}\n"

        try:
            send_mail(
                subject=f"Yeni Sipariş Geldi - #{order.id}",
                message=f"""
Yeni bir sipariş oluşturuldu.

Müşteri: {full_name}
Telefon: {phone}
Adres: {address}

Ürünler:
{order_products_text}

Toplam Tutar: ₺{total}
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_ORDER_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            print("Mail gönderilemedi:", e)

        request.session['cart'] = {}
        return redirect('order_success')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


def increase_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart
    return redirect('cart')


def decrease_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')


def order_success(request):
    return render(request, 'store/order_success.html')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'store/my_orders.html', {
        'orders': orders,
    })


@login_required(login_url='login')
def add_review(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment,
        )

    return redirect('product_detail', id=product.id)


@login_required(login_url='login')
def toggle_favorite(request, id):
    product = get_object_or_404(Product, id=id)

    favorite = Favorite.objects.filter(
        user=request.user,
        product=product,
    )

    if favorite.exists():
        favorite.delete()
    else:
        Favorite.objects.create(
            user=request.user,
            product=product,
        )

    return redirect('product_detail', id=product.id)


@login_required(login_url='login')
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)

    return render(request, 'store/my_favorites.html', {
        'favorites': favorites,
    })


@staff_member_required
def dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_revenue = sum(order.total_price for order in Order.objects.all())
    latest_orders = Order.objects.order_by('-created_at')[:5]

    return render(request, 'store/dashboard.html', {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'latest_orders': latest_orders,
    })


@staff_member_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')

        category = Category.objects.first()

        Product.objects.create(
            category=category,
            name=name,
            price=price,
            description=description,
            stock=stock,
            image=image,
            is_active=True,
        )

        return redirect('home')

    return render(request, 'store/add_product.html')


def contact(request):
    return render(request, 'store/contact.html')