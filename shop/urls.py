from django.urls import path
from . import views


urlpatterns = [
    #-----------------------Home--------------------------------
    path('', views.index, name='home'),
    #-----------------------Shop-------------------------------- 
    path('shop', views.shop, name='shop'),
    path('sorting/<slug:key_name>/', views.sorting, name='sorting'),
    #-----------------------Product details--------------------------------
    path('detail/<int:id>/', views.product_detail, name='detail'),
    # path('rate/<int:product_id>/<int:rating>/', views.rate),
    #-----------------------Cart--------------------------------
    path('cart/', views.cart, name='cart'),
    path('to-card/<int:product_id>/<str:action>/', views.to_cart, name='to_card'),
    path('clear-cart', views.clear_cart, name='clear_cart'),
    path('check-out', views.checkout, name='checkout'),
    #---------------------Login, Logout and Register--------------------
    path('register', views.register, name='register'),
    path('login/',views.log_in,name='login'),
    path('logout/',views.log_out,name='log_out'),
    #-----------Errorlar--------------------
    path('error/',views.error,name='error'),
    path('error2/',views.error2,name='error2'),
    #--------------------My Account--------------------
    path('accaunt/', views.profile, name='accaunt'),
    #----------Checkout and payment--------------------
    path('payment/',views.create_checkout_sessions, name='payment'),
    path('success/', views.success_payment, name='success'),
]