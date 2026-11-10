from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .pagination import StandardResultsSetPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from .forms import ProductForm, CategoryForm


def admin_required(view_func):
    """Decorator to ensure user is logged in AND is an admin/superuser."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access this page.")
            return redirect('login')
        if not request.user.is_superuser:
            messages.error(
                request,
                "Access Denied: You do not have permission to perform this action."
            )
            return redirect('product_list')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def home(request):
    """Home view displaying featured/recent products."""
    recent_products = Product.objects.all().order_by('-id')[:4]
    context = {
        'recent_products': recent_products
    }
    return render(
        request,
        'products/home.html',
        context
    )


@login_required
def dashboard(request):
    """Dashboard view for authenticated users."""
    return render(
        request,
        'accounts/dashboard.html',
        {'user': request.user}
    )


def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(
        request,
        'products/product_list.html',
        context
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(
        request,
        'products/product_detail.html',
        context
    )


def category_list(request):
    categories = Category.objects.annotate(
        product_count=Count('products')
    )
    context = {
        'categories': categories
    }
    return render(
        request,
        'products/category_list.html',
        context
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products
    }
    return render(
        request,
        'products/category_detail.html',
        context
    )


# === CREATE ===
@admin_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(
        request,
        'products/product_form.html',
        {'form': form}
    )


# === UPDATE ===
@admin_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'products/product_form.html',
        {'form': form}
    )


# === DELETE ===
@admin_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'{product_name} deleted successfully!')
        return redirect('product_list')

    return render(
        request,
        'products/product_confirm_delete.html',
        {'product': product}
    )


# ============================================================
# API VIEWS (Module 14 - Complete)
# ============================================================

class ProductListCreateAPIView(ListCreateAPIView):
    """
    GET  /api/products/  → List all products (paginated + filterable)
    POST /api/products/  → Create a new product (authenticated users only)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'category__name']
    ordering_fields = ['price', 'created_at', 'stock']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        # Automatically set the logged-in user as the creator
        serializer.save(created_by=self.request.user)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET    /api/products/<id>/  → Retrieve single product
    PUT    /api/products/<id>/  → Full update (owner only)
    PATCH  /api/products/<id>/  → Partial update (owner only)
    DELETE /api/products/<id>/  → Delete (owner only)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CategoryListAPIView(APIView):
    """
    GET /api/categories/  → List all categories with product count
    """
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)