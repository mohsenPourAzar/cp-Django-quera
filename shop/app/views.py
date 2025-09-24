from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Order

def checkout(request, order_pk):
    
    order = get_object_or_404(Order, pk=order_pk)

    items = order.orderitem_set.all()
    # orderitem_set is the reverse relation from Order to OrderItem and
    # retrieves all OrderItem instances related to the given Order instance.
    
    total = 0

    for item in items:
        line_total = item.product.price * item.quantity
        total = total + line_total

    return JsonResponse({"total_price": "%.2f" % total})
