import json
from functools import wraps
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, logout
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

import stripe

from .models import Category, Product, Response
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Create your views here.


def add_categories(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        index = 1 if isinstance(args[0], TemplateView) else 0
        try:
            args[index].data['categories'] = Category.objects.all()
        except:
            args[index].data = {'categories': Category.objects.all()}
        return function(*args, **kwargs)
    return wrap


class IndexView(TemplateView):
    template_name = 'shop-templates/index.html'

    @add_categories
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {**request.data})


class LoginView(TemplateView):
    template_name = 'user-templates/login.html'

    @add_categories
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:home')
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {**request.data, 'form': form})

    @add_categories
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:home')
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('main:home')
        return render(request, self.template_name, {**request.data, 'form': form})


class RegistrationView(TemplateView):
    template_name = 'user-templates/registration.html'

    @add_categories
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:home')
        form = CustomUserCreationForm()
        return render(request, self.template_name, {**request.data, 'form': form})

    @add_categories
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:home')
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
        return render(request, self.template_name, {**request.data, 'form': form})


def logout_controller(request):
    logout(request)
    return redirect('main:home')


@add_categories
def about_controller(request):
    return render(request, 'shop-templates/about.html', {**request.data})


@add_categories
def category_controller(request, name: str):
    category = Category.objects.get(name=name.title())
    products = Product.objects.filter(category=category)
    return render(request, 'shop-templates/category.html', {**request.data, 'category': category, 'products': products})


@add_categories
def product_controller(request, id: int):
    product = Product.objects.get(id=id)
    responses = Response.objects.filter(product=product).order_by('-date')
    return render(request, 'shop-templates/product.html', {**request.data, 'product': product, 'responses': responses})


def comment_controller(request, id: int):
    if request.method == 'POST':
        response = Response()
        response.text = request.POST.get('text')
        response.user = request.user
        response.product = Product.objects.get(id=id)
        response.save()
    return redirect('main:product', id=id)


def product_amount_controller(request, id: int):
    amount = Product.objects.get(id=id).amount
    return HttpResponse(amount)


def get_product_controller(request, id):
    result = Product.objects.get(id=id)
    return JsonResponse({
        'name': result.name,
        'price': result.price,
        'imageURL': result.images.all()[0].image.url
    })


@add_categories
def cart_controller(request):
    return render(request, 'shop-templates/cart.html', {**request.data, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})


@csrf_exempt
def create_checkout_session(request):
    request_data = json.loads(request.body)
    items = []
    for id, count in request_data.items():
        p = Product.objects.get(id=id)
        items.append({
            'price_data': {
                'currency': 'uah',
                'product_data': {
                    'name': p.name,
                },
                'unit_amount': int(p.price * 100),
            },
            'quantity': count,
        })
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url=request.build_absolute_uri(
                reverse('main:paysuccess')
            ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('main:paycancel')),
    )

    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "shop-templates/pay-success.html"

    @add_categories
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {**request.data})


class PaymentCancelView(TemplateView):
    template_name = "shop-templates/pay-cancel.html"

    @add_categories
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {**request.data})