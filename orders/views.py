from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Order, OrderItem
from cart.models import Cart


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        return redirect("cart")

    total_price = sum(
        item.product.price * item.quantity
        for item in cart.items.all()
    )

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            total_price=total_price,
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        cart.items.all().delete()

        return redirect("order_success", order_id=order.id)

    context = {
        "cart": cart,
        "total_price": total_price,
    }

    return render(request, "orders/checkout.html", context)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "orders/order_success.html",
        {"order": order}
    )