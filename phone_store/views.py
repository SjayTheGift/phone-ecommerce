import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .models import Product, ShippingAddress
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from .forms import ShippingAddressForm
from .utils import cartData, createOrder    



def home(request):
    cart_data = cartData(request)
    order = cart_data['order']
    items = cart_data['items']
    cartItems = cart_data['cartItems']

    product = Product.objects.all()
    context = {
        'products' : product,
        'order': order,
        'items': items,
        'cartItems': cartItems,
    }

    return render(request, template_name='index.html', context=context)


def cart(request):
    cart_data = cartData(request)
    order = cart_data['order']
    items = cart_data['items']
    cartItems = cart_data['cartItems']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, template_name='checkout.html', context=context)


def updateItem(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    if request.user.is_authenticated:
        create_order = createOrder(request, product_id)
        order_item = create_order['order_item']
    else:
        pass

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -=1

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse('Item was added', safe=False)


def deleteItem(request):
    data = json.loads(request.body)
    product_id = data['productId']

    if request.user.is_authenticated:
        create_order = createOrder(request, product_id)
        order_item = create_order['order_item']
    else:
        pass
    order_item.delete()

    return JsonResponse('Item was deleted', safe=False)

@login_required
def checkout(request):
    cart_data = cartData(request)
    order = cart_data['order']
    

    if request.method == 'GET':
        form = ShippingAddressForm()

        shippingAddress = ShippingAddress.objects.filter(customer=request.user.customer, order=order)

        return render(request, template_name='shipping.html', context={"form": form, "order": order, "shippingAddress": shippingAddress})
    
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        # print(form)
        if form.is_valid():
            address = form.save(commit=False)
            
            customer = request.user.customer
            # print(f'address: {address} {address.user}')
            address.customer = customer
            address.order = order
            address.save()
            return HttpResponseRedirect('/checkout/')
        # return render(request, template_name='shipping.html', context={"form": form, "order": order})
    else:
        form = ShippingAddressForm()
   
    return render(request, template_name='shipping.html', context={"form": form, "order": order})


def chooseAddress(request):
    return JsonResponse('Address was chossen', safe=False)