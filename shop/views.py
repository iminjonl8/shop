from django.views.generic import ListView
from .models import Product
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import redirect, render
from .models import Cart, CartItem, Product
from .models import Cart
from .models import Cart, Order
from .models import Order
from django.views.generic import CreateView
from .forms import ProductForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic import DeleteView




class HomeView(TemplateView):
    template_name = 'authenticate/home.html'




class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    
class AddToCartView(View):
    def post(self, request, product_id):
        cart_id = request.session.get('cart_id')
        if not cart_id:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.get(id=cart_id)
        
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            return render(request, 'product_list.html', {
                'products': Product.objects.all(),
                'error_message': f"{product.name} uchun zaxira yetarli emas."
            })
        
        return redirect('product_list')

class ViewCartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id')
        cart = Cart.objects.get(id=cart_id) if cart_id else None
        cart_items = cart.cartitem_set.all() if cart else []
        context['cart_items'] = cart_items
        context['cart'] = cart
        context['total_price'] = cart.get_total_price() if cart else 0
        return context
    
    

class PlaceOrderView(View):
    def post(self, request):
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = None

            if cart and cart.cartitem_set.exists():
                order, created = Order.objects.get_or_create(cart=cart)
                if created:
                    request.session.pop('cart_id', None)
                    return redirect('order_success')
                else:
                    return render(request, 'order_history.html', {
                        'orders': Order.objects.all(),
                        'error_message': "Bu savatcha uchun buyurtma allaqachon yaratilgan."
                    })
            else:
                request.session.pop('cart_id', None)
                return redirect('product_list')
        return redirect('product_list')  


class ClearCartView(View):
    def post(self, request):
        request.session.pop('cart_id', None)
        return redirect('product_list')


class OrderHistoryView(ListView):
    model = Order
    template_name = 'order_history.html'
    context_object_name = 'orders'


class DeleteOrderView(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        return redirect('order_history')




class AddProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('product_list')


class EditProductView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'edit_product.html'
    success_url = reverse_lazy('product_list')

class DeleteProductView(DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('product_list')


from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm 


def login_user (request):
	if request.method == 'POST': #if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:# if user exist
			login(request, user)
			messages.success(request,('Youre logged in'))
			return redirect('home') #routes to 'home' on successful login  
		else:
			messages.success(request,('Error logging in'))
			return redirect('login') #re routes to login page upon unsucessful login
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request,('Youre now logged out'))
	return redirect('home')

def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ('Youre now registered'))
			return redirect('home')
	else: 
		form = SignUpForm() 

	context = {'form': form}
	return render(request, 'authenticate/register.html', context)


def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You have edited your profile'))
			return redirect('home')
	else: 		
		form = EditProfileForm(instance= request.user) 

	context = {'form': form}
	return render(request, 'authenticate/edit_profile.html', context)
	



def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You have edited your password'))
			return redirect('home')
	else: 		
		form = PasswordChangeForm(user= request.user) 

	context = {'form': form}
	return render(request, 'authenticate/change_password.html', context)