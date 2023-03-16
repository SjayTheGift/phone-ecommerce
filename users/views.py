import json

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from .forms import UserUpdateForm, MyCustomSignupForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, HttpResponseRedirect

from .models import User
from phone_store.utils import cartData
from phone_store.models import *


class MyLoginView(LoginView):
    template_name = 'account/login.html'

    def get(self, request):
        form = AuthenticationForm()
        cart_data = cartData(request)
        order = cart_data['order']
        context = {
            'form': form,
            'order': order,
        }
        
        return render(request, self.template_name, context)

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        email = form.get_user()
        user = User.objects.get(email=email)
        if user.is_active:
            auth_login(self.request, form.get_user())
            try:
                cart = json.loads(self.request.COOKIES.get('cart', 1))
            except:
                cart = {}
            if len(cart) > 0:
                print(cart)
                for i in cart:
                    quantity = cart[i]['quantity']
                    customer = self.request.user.customer
                    
                    product = Product.objects.get(id=i)

                    order, created  = Order.objects.get_or_create(customer=customer, complete=False)
                    items = OrderItem.objects.all().filter(customer=customer, order=order, product=product).exists()

                    if(items):
                        items = OrderItem.objects.all()
                        for item in items:
                            quantity += item.quantity

                        if product:
                            OrderItem.objects.update(quantity=quantity)
                    else:
                        order_item, created = OrderItem.objects.get_or_create(customer=customer, order=order, product=product, quantity=quantity)
                    response = HttpResponseRedirect('/')
                    response.delete_cookie('cart')         
            else:
                response = HttpResponseRedirect('/')
        return response



class RegisterView(generic.CreateView):

    def get(self, request, *args, **kwargs):
        form = MyCustomSignupForm()
        cart_data = cartData(request)
        order = cart_data['order']
        context = {
            'form': form,
            'order': order,
        }
        return render(request, 'account/signup.html', context)

    def post(self, request, *args, **kwargs):
        form = MyCustomSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, f'Account has been created successfullly')
            return redirect('account_login')
        return render(request, 'account/signup.html', {'form': form})


class ProfileView(LoginRequiredMixin, generic.View):
    template_name = 'account/profile.html'

    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        cart_data = cartData(request)
        order = cart_data['order']
        context = {
            'u_form': u_form,
            'order': order,
        }
        
        return render(request, self.template_name, context)

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
        else:
            messages.error(request, f'Your account has not been updated!')
        return redirect('profile')


def change_password(request):
    if request.method == 'GET':
        form = PasswordChangeForm(request.user)
        cart_data = cartData(request)
        order = cart_data['order']
        context = {
            'form': form,
            'order': order,
        }
        
        return render(request, 'account/password_change.html', context=context)

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.warning(
                request, 'There was an error changing your password!')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'account/password_change.html', {'form': form})
