from django.urls import path
from django.conf import settings
from django.conf.urls.static  import static
from .views import (
    HomeView,
    ProductListView,
    AddToCartView,
    ViewCartView,
    OrderHistoryView,
    AddProductView,
    EditProductView,
    DeleteProductView,
    PlaceOrderView,
    DeleteOrderView,
    login_user,
    logout_user,
    register_user,
    edit_profile,
    change_password
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', ViewCartView.as_view(), name='view_cart'),
    path('order/history/', OrderHistoryView.as_view(), name='order_history'),
    path('product/add/', AddProductView.as_view(), name='add_product'),
    path('product/edit/<int:product_id>/', EditProductView.as_view(), name='edit_product'),
    path('product/delete/<int:product_id>/', DeleteProductView.as_view(), name='delete_product'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('change_password/', change_password, name='change_password'),
    path('order/place/', PlaceOrderView.as_view(), name='place_order'),
    path('order/delete/<int:order_id>/', DeleteOrderView.as_view(), name='delete_order'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
