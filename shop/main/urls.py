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
    path('cart', cart_controller, name='cart'),
    #тут мене бомбонуло
    #18:40
    path('product/get/description/<int:id>', getdescription,name="getdescrib"),
    path('product/get/image/<int:id>', getimage,name="getimg"),
    path('product/get/name/<int:id>', getname,name="getname"),
    path('product/get/price/<int:id>', getprice,name="getprice"),
    path('product-amount/<int:id>', product_amount_controller, name='productamount'),
    # account-paths
    path('account/login', LoginView.as_view(), name='login'),
    path('account/registration', RegistrationView.as_view(), name='registration'),
    path('account/logout', logout_controller, name='logout'),
]
