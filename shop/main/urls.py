from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    # shop-paths
    path('', IndexView.as_view(), name='home'),
    path('about', about_controller, name='about'),
    path('categories/<str:name>', category_controller, name='categories'),
    path('product/<int:id>', product_controller, name='product'),
    path('comment/<int:id>', comment_controller, name='comment'),
    path('product-amount/<int:id>', product_amount_controller, name='productamount'),
    path('get-product/<int:id>', get_product_controller, name='productamount'),
    path('cart', cart_controller, name='cart'),
    # pay
    path('get-signature', get_signature_controller, name='signature'),
    # account-paths
    path('account/login', LoginView.as_view(), name='login'),
    path('account/registration', RegistrationView.as_view(), name='registration'),
    path('account/logout', logout_controller, name='logout'),
]
