from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('post/', views.ProductCreateView.as_view(), name='product-post'),
    path('my-products/', views.MyProductListView.as_view(), name='my-products'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('buy/<int:pk>/', views.BuyProductView.as_view(), name='buy-product'),
    path('transactions/', views.TransactionView.as_view(), name='transactions'),
    path('cart/', views.CartView.as_view(), name='cart'),
path('add-to-cart/<int:pk>/', views.AddToCartView.as_view(), name='add-to-cart'),
path('remove-from-cart/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
path('cart/buy/', views.BuyCartView.as_view(), name='buy-cart'),


]
