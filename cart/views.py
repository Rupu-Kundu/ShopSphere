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

    total_price = sum(
        item.product.price * item.quantity
        for item in cart.items.all()
    )

    return render(request, "cart/cart.html", {
        "cart": cart,
        "total_price": total_price,
    })


def update_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    quantity = int(request.POST.get("quantity", 1))

    if quantity > 0:
        if quantity <= cart_item.product.stock:
            cart_item.quantity = quantity
            cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart")


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    return redirect("cart")