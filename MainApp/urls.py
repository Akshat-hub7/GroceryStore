from django.urls import path
from . import views

urlpatterns = [
    # General Access
    path('', views.shop, name='shop'),  # Landing or Shop page
    path('dashboard/', views.dashboard, name='dashboard'),  # User dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard

    # Product & Orders
    path('products/', views.products, name='products'),  # Product listing
    path('add-product/', views.add_product, name='add_product'),  # Admin: Add product
    path('manage-orders/', views.manage_orders, name='manage_orders'),  # Admin: Manage orders
    path('place-order/', views.place_order, name='place_order'),  # Place order
    path('orders/', views.order_list, name='order_list'),  # View user's order history
    path('product/<int:product_id>/', views.product_detail, name='products_detail'),
    path('category/<slug:category_slug>/', views.category_filter, name='category_filter'),


    # Cart
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),


    # Authentication
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
