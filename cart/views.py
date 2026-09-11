from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem
from products.models import Product


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )


    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    return render(request, "cart/cart.html", {
        "cart": cart,
    })