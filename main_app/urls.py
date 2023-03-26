from django.contrib import admin
from django.urls import path
from .views import * 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view


urlpatterns = [
    # path('base/', base, name="base"),
    # path('', ProductView),
    path('', ProductView.as_view(), name='home'),  # class based view url
    
    path('product-detail/<int:id>/', ProductDetailView.as_view(), name='product-detail'),  #<int:pk>
    path('cart', cart, name='cart'), 
    path('add_to_cart/<int:id>/', add_to_cart, name='add-to-cart'),
    path('buy/', buy_now, name='buy-now'),
    path('profile/', profile, name='profile'),
    path('address/', address, name='address'),
    path('orders/', orders, name='orders'),
    # path('changepassword/', change_password, name='changepassword'),

    path('mobile/', mobile, name='mobile'),
    path('mobile/<slug:data>', mobile, name='mobiledata'),

    path('login/', user_login, name='login'), # views for html and views login  --> self made
    # path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'), # used for django inbuilt login form
    
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'), # django inbuilt logout only url needed

    # path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm), name='passwordchange'),
    path('passwordchange/', password_change, name='passwordchange'),

    # path('registration/', customerregistration, name='customerregistration'),
    path('registration/', CustomerRegistrationView.as_view(), name='customerregistration'),

    path('checkout/', checkout, name='checkout'),

    path('plus_qty/<int:id>/', plus_qty, name='plus_qty'),
    path('minus_qty/<int:id>/', minus_qty, name='minus_qty'),
    path('remove_item/<int:id>/', remove_item, name='remove_item'),
    path('401/',error_401, name='error_401'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # to show  image in frontend
