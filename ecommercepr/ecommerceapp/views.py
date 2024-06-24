# ecommerceapp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, CartItem, Cart

def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))
    request.session['cart_id'] = cart.id
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'Added {product.name} to your cart.')
    return redirect('cart')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


def cart(request):
    cart_id = request.session.get('cart_id')
    cart_items_with_totals = []
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            total_price = item.quantity * item.product.price
            cart_items_with_totals.append({
                'item': item,
                'total_price': total_price
            })
        total = sum(item['total_price'] for item in cart_items_with_totals)
    else:
        total = 0

    context = {
        'cart_items_with_totals': cart_items_with_totals,
        'total': total
    }
    return render(request, 'store/cart.html', context)