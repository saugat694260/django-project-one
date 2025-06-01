from django.views.generic import CreateView,ListView,DeleteView,UpdateView,DetailView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import Http404
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart, CartItem


def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('product-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 5  # Show 5 products per page

    def get_queryset(self):
        queryset = Product.objects.all()

        # Exclude user's own products
        if self.request.user.is_authenticated:
            queryset = queryset.exclude(user=self.request.user)

        search_query = self.request.GET.get('q')
        category_filter = self.request.GET.get('category')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if category_filter and category_filter != 'all':
            queryset = queryset.filter(category=category_filter)

        return queryset

    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_object()
        user = self.request.user

        context['in_cart'] = False

        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            context['in_cart'] = cart.items.filter(product=product).exists()

        return context

class BuyProductView(View):
    def post(self, request, pk):
        # Here you'd handle payment or order logic in future
        return redirect(reverse('transactions'))
    
class TransactionView(TemplateView):
    template_name = 'store/transactions.html'

class MyProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'store/my_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)
    
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('my-products')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise Http404()
        return obj
    
from django.views.generic.edit import DeleteView

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy('my-products')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise Http404()
        return obj
    
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart = get_or_create_cart(request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart')
    
class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request.user)
        context['cart_items'] = cart.items.select_related('product').all()
        context['total_price'] = cart.total_price()
        return context
    
class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cart = get_or_create_cart(request.user)
        cart.items.filter(product_id=pk).delete()
        return redirect('cart')

class BuyCartView(LoginRequiredMixin, View):
    def post(self, request):
        cart = get_or_create_cart(request.user)
        # Here you'd handle actual transaction logic (order creation etc.)

        # (Optional) Clear the cart after buying
        cart.items.all().delete()

        return redirect('transactions')


