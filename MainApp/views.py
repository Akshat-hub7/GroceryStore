from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Products, Cart, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from users.forms import CustomUserCreationForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not authorized to view this page.")

    orders = Order.objects.all().order_by('-ordered_at')  # Recent orders first
    return render(request, 'admin_dashboard.html', {'orders': orders})

@login_required
def dashboard(request):
    products = Products.objects.all()
    categories = Products.CATEGORY_CHOICES
    return render(request, 'product.html', {'products': products, 'category_choices': categories})

def shop(request):
    products = Products.objects.all()
    categories = Products.CATEGORY_CHOICES
    return render(request, 'shop.html', {'products': products, 'category_choices': categories})

def product_detail(request, product_id):
    product = get_object_or_404(Products, product_id=product_id)
    return render(request, 'product_detail.html', {'product': product})



def products(request):
    products = Products.objects.all()
    return render(request, 'products.html', {'products': products})

@login_required
def manage_orders(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can manage orders.")
    
    orders = Order.objects.all()
    return render(request, 'manage_orders.html', {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,  # ✅ Add this line
    })






@login_required
def add_product(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can add products.")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # ✅ <- include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # DO NOT manually set the password here
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            if (user.user_type == 'admin' and user.is_superuser) or (user.user_type == 'user' and not user.is_superuser):
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Make sure this matches a valid route

# Add Product (Admin or Staff)
@login_required
def product_create(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to add products.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

# Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.products.add(product)
    messages.success(request, f"{product.product_name} added to cart.")
    return redirect('dashboard')

@login_required
def get_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return cart

# View Cart
@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Products, product_id=product_id)
    cart.products.add(product)
    messages.success(request, f"{product.product_name} added to cart.")
    return redirect('view_cart')

# Remove from Cart
@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Products, pk=product_id)
    cart.products.remove(product)
    messages.success(request, f"{product.product_name} removed from cart.")
    return redirect('view_cart')

# Create Order
@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    if cart.products.exists():
        order = Order.objects.create(user=request.user)
        order.products.set(cart.products.all())
        cart.products.clear()
        messages.success(request, "Order placed successfully!")
        return redirect('order_list')
    else:
        messages.warning(request, "Your cart is empty!")
        return redirect('dashboard')

# View Orders
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'order_list.html', {'orders': orders})


@require_POST
@login_required
def update_order_status(request, order_id):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can update order status.")
    
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
        messages.success(request, f"Order #{order.id} status updated to {new_status}.")
    else:
        messages.error(request, "Invalid status value.")

    return HttpResponseRedirect(reverse('manage_orders'))


def category_filter(request, category_slug):
    filtered_products = Products.objects.filter(category=category_slug)
    categories = Products.CATEGORY_CHOICES
    return render(request, 'category_products.html', {
        'products': filtered_products,
        'category_name': dict(Products.CATEGORY_CHOICES).get(category_slug, category_slug),
        'category_choices': categories,
    })



@login_required
def edit_product(request, product_id):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can edit products.")

    product = get_object_or_404(Products, product_id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})



@login_required
def delete_product(request, product_id):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Only admins can delete products.")

    product = get_object_or_404(Products, product_id=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('dashboard')

    return render(request, 'confirm_delete.html', {'product': product})
