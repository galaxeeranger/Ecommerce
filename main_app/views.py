from django.views import View
from .models import *
from .forms import CustomerRegistrationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage




# def base(request):
#     cart_count=Cart.objects.filter(user_id=request.user.id).count()
#     print(cart_count)
#     return render(request,'base.html', {'cart_count': cart_count})

def error_401(request):
    return render(request, '401.html')

# def ProductView(request):
#     data=Product.objects.all()
#     return render(request, 'home.html',{'data':data})


class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        # print(bottomwears,'BBBBBBBBBBBBBBBBBBB')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        context={
            'topwears':topwears, 
            'bottomwears':bottomwears, 
            'mobiles':mobiles, 
            'laptops':laptops,
            'cart_count':Cart.objects.filter(user_id=request.user.id).count()
            }
        return render(request, 'home.html', context)


# def product_detail(request):
    # return render(request, 'productdetail.html')

class ProductDetailView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            product = Product.objects.get(id=id)
            context = {
                'product':product,
                'cart_count':Cart.objects.filter(user_id=request.user.id).count()
            }
            return render(request, 'productdetail.html', context)
        return redirect('/401/')

    
def cart(request):
    if request.user.is_authenticated:
        sub_total = 0
        shipping_total = 70
        cal=Cart.objects.filter(user=request.user.id)
        for i in cal:
            sub_total = (i.product.discounted_price * i.quantity) + sub_total

        shipping_total = shipping_total + sub_total

        context = {
            'sub_total':sub_total,
            'shipping_total':shipping_total,
            'cart':Cart.objects.filter(user=request.user.id),
            'cart_count':Cart.objects.filter(user_id=request.user.id).count()
        }
        return render(request, 'addtocart.html', context)
    return redirect('/401/')


def add_to_cart(request,id):
    if request.user.is_authenticated:
        product_id = Product.objects.get(id=id)

        if Cart.objects.filter(user_id=request.user.id,product=product_id).exists():
            messages.success(request, "Product already exists.")
            context = {
                'cart':Cart.objects.filter(user__id=request.user.id),
                'cart_count':Cart.objects.filter(user_id=request.user.id).count()
            }
            return redirect('/cart', context)
        else:
            cart = Cart.objects.create(user_id=request.user.id, product=product_id, quantity = 1)
            cart.save()
            messages.success(request, "Product added to your cart")
            context = {
                'cart':Cart.objects.filter(user__id=request.user.id),
                'cart_count':Cart.objects.filter(user_id=request.user.id).count()
            }
            return redirect('/cart', context)
    return redirect('/401/')


def buy_now(request):
    if request.user.is_authenticated:
        context = {
            'cart_count':Cart.objects.filter(user_id=request.user.id).count()
        }
        return render(request, 'buynow.html', context)
    return redirect('/401/')


def profile(request):
    if request.user.is_authenticated:
        context = {
            'cart_count':Cart.objects.filter(user_id=request.user.id).count()
        }
        return render(request, 'profile.html', context)
    return redirect('/401/')
    

def address(request):
    if request.user.is_authenticated:
        context = {
            'cart_count':Cart.objects.filter(user_id=request.user.id).count()
        }
        return render(request, 'address.html', context)
    return redirect('/401/')
   

def orders(request):
    if request.user.is_authenticated:
        context = {
            'cart_count':Cart.objects.filter(user_id=request.user.id).count()
        }
        return render(request, 'orders.html', context)
    return redirect('/401/')
    

# def change_password(request):
#     return render(request, 'changepassword.html')
@csrf_exempt
def password_change(request):                       # if using django inbuilt form only write url no need of views
    if request.user.is_authenticated:
        if request.method =='POST':
            oldpassword=request.POST.get('op')
            password1 = request.POST.get('np')
            password2 = request.POST.get('cnp')
            valid_cp=authenticate(old_password=oldpassword,password1=password1,password2=password2)
            if valid_cp is not None:
                login(request, valid_cp)
                return redirect('/profile')
            else:
                return render(request, 'passwordchange.html')
        return render(request, 'passwordchange.html')
    return redirect('/401/')


# catogery example u can make more similarly
def mobile(request, data=None):  # filtering by brands
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Xiomi' or data == 'Samsung' or data == 'Apple' or data == 'Oppo' or data == 'OnePlus':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=15000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=15000)
    context = {
        'mobiles': mobiles,
        'cart_count':Cart.objects.filter(user_id=request.user.id).count()
        }
    return render(request, 'mobile.html', context)

def user_login(request):                       # if using django inbuilt form only write url no need of views
    if request.method =='POST':
        username=request.POST.get('un')
        password = request.POST.get('ps')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile')
        else:
            # context = {'msg': 'Invalid username or password'}
            return render(request, 'login.html')

    return render(request, 'login.html')


class CustomerRegistrationView(View):
    def get(self, request): # form with empty data
        form = CustomerRegistrationForm()
        return render(request, 'customerregistration.html', {'form':form})

    def post(self,request): # form with fill data
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            text_content = 'Congratulation!! You have Registered Successfully. To ECOMMERCE'
            email = form.cleaned_data['email']
            subject = "ECOMMERCE"
            thoughts = "{} by {}".format(text_content,email)
            sender = 'shivmurathgupta@gmail.com'
            msg = EmailMessage(subject, thoughts, sender, [email])
            msg.content_subtype = "text"  # Main content is now text/html
            msg.send()
            messages.success(request, "Congratulation!! Registered Successfully")
            form.save()
        return render(request, 'customerregistration.html', {'form':form}) 


def checkout(request):
    if request.user.is_authenticated:
        context = {
            'cart_count':Cart.objects.filter(user_id=request.user.id).count()
        }
        return render(request, 'checkout.html', context)
    return redirect('/401/')
    

def plus_qty(request, id):
    if request.user.is_authenticated:
        add_qty = Cart.objects.get(id=id)
        add_qty.quantity = add_qty.quantity + 1
        add_qty.save()
        base  ="http://127.0.0.1:8000/"
        context = {
            'base':base,
            'cart':Cart.objects.filter(user__id=request.user.id),
            'cart_count':Cart.objects.filter(user_id=request.user.id).count()
        }
        return redirect('/cart', context)
    return redirect('/401/')


def minus_qty(request, id):
    if request.user.is_authenticated:
        sub_qty = Cart.objects.get(id=id)
        base  ="http://127.0.0.1:8000/"
        if sub_qty.quantity > 1:
            sub_qty.quantity = int(sub_qty.quantity - 1)
            sub_qty.save()

        context = {
            'base':base,
            'cart':Cart.objects.filter(user__id=request.user.id),
            'cart_count':Cart.objects.filter(user_id=request.user.id).count()
        }
        return redirect('/cart', context)
    return redirect('/401/')


def remove_item(request, id):
    if request.user.is_authenticated:
        item = Cart.objects.get(id=id)
        item.delete()
        context = {
            'cart':Cart.objects.filter(user__id=request.user.id),
            'cart_count':Cart.objects.filter(user_id=request.user.id).count()
        }
        return redirect('/cart', context)
    return redirect('/401/')

