from phone_store.models import *
import json

def getItems(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', 1))
    except:
        cart = {}
        if len(cart) > 0:
            for i in cart:
                quantity = cart[i]['quantity']
                customer = request.user.customer
                product = Product.objects.get(id=i)
                order, created  = Order.objects.get_or_create(customer=customer, complete=False)
                order_item, created = OrderItem.objects.get_or_create(order=order, product=product, quantity=quantity)   
        else:
            pass
    return{
        'order_item': order_item,
        'order': order,
    }