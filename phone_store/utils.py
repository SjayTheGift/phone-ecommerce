import json
from .models import Product, Order, OrderItem

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', 1))
    except:
        cart = {}
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    items = []
    cartItems = order['get_cart_items']
    for i in cart:
        cartItems += cart[i]['quantity']
        product = Product.objects.get(id=i)
        total = (product.price * cart[i]['quantity'])

        order['get_cart_total'] += total
        order['get_cart_items'] = cartItems

        item = {
            'product' :{
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image': product.image,
            },
            'quantity': cart[i]['quantity'],
            'get_total': total,
        }

        items.append(item)
    return {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookie_data = cookieCart(request)
        items = cookie_data['items']
        order = cookie_data['order']
        cartItems = cookie_data['cartItems']
    
    return{
        'order': order,
        'items': items,
        'cartItems': cartItems,
    }


def createOrder(request, id):
    customer = request.user.customer
    product = Product.objects.get(id=id)
    order, created  = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    return{
        'order': order,
        'order_item': order_item,
    }