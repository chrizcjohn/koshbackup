from django.shortcuts import redirect, render
from .models import *
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
import re
from django.views import View
from .middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
import json
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template.loader import render_to_string

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
SpecialSym = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
pat = re.compile(SpecialSym) 
# Create your views here.

class Index(View):
    def get(self, request):
        context = {}
        print(request.session.get('email'))
        return render(request, 'index.html', context)


class Store(View):
    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] ={}
        products = None
        categories = Category.objects.all()
        categoryID= request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_id(categoryID)
        else:
            products = Product.get_all_products()

        context = {'products': products, 'categories':categories}
        return render(request, 'store.html', context)

    def post(self,request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        print(cart)
        request.session['cart'] =cart
        return redirect('store')


   
        
    



class Cart(View):
    def get(self, request):
            
            if 'cart' not in request.session:
                request.session['cart'] = None
                return render(request, 'cart.html')
            else:
                ids = list(request.session.get('cart').keys())

                products = Product.get_products_by_id(ids)
                if len(products) == 0:
                    print("no value")
                else:
                    print('value is there')
                return render(request, 'cart.html', {'products': products})
        

    



class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                
                
                return redirect('index')
            else:
                error_message = 'Email or password invalid!'
        else:
            error_message = 'Email or password invalid!'
        
        print(email,password)
        return render(request,'login.html',{'error':error_message})


        

def validateCustomer(customer):
    error_message = None
    if (not customer.name):
            error_message = "First name Required !!"
    elif len(customer.name) < 4:
                error_message = "First name must be 4 Characters or more  "
    elif not customer.phone:
            error_message   = " Phone number is required "
    elif len(customer.phone) < 10 or len(customer.phone) > 10:
            error_message = " Phone number must be 10 char Long"
    elif not re.search(regex, customer.email):
            error_message = " Enter valid email id"

    # PASSOWORD VALIDATION    
    elif len(customer.password) < 8:
            error_message = "Password should be 8 char long"
    # elif not re.search(pat, customer.password):
    #         error_message="Password should contain Uppper case character, lower case character, special character and at least a number"
    elif customer.isExists():
        error_message = "Email address already exists"

    return error_message


class Signup(View):
    def get(self, request):
        return render(request, 'registration.html')

    def post(self, request):
        postDATA = request.POST
        fullname = postDATA.get('fullname')
        email = postDATA.get('email')
        phone = postDATA.get('Phone')
        password = postDATA.get('password')
        #VALIDATION

        value = {
            'fullname': fullname,
            'email': email,
            'phone': phone,
            
        }
        
        error_message = None
        

        customer = Customer(name=fullname,
                                email=email,
                                phone=phone,
                                password=password)
        
        error_message =  validateCustomer(customer)
        if not error_message: 

            
            customer.password = make_password(customer.password)
            customer.register()
            # return redirect('store')
            return redirect('index')
        else:
            data = {
             'error': error_message,
             'value':value
            }
            return render(request, 'registration.html', data)

# def signup(request):
    
    # if request.method =='GET':
    #     return render(request, 'registration.html')
    # else:
    #     postDATA = request.POST
    #     fullname = postDATA.get('fullname')
    #     email = postDATA.get('email')
    #     phone = postDATA.get('Phone')
    #     password = postDATA.get('password')
    #     #VALIDATION

    #     value = {
    #         'fullname': fullname,
    #         'email': email,
    #         'phone': phone,
    #     }
        
    #     error_message = None
        

    #     customer = Customer(name=fullname,
    #                             email=email,
    #                             phone=phone,
    #                             password=password)
        
    #     error_message =  validateCustomer(customer)
    #     if not error_message: 

            
    #         customer.password = make_password(customer.password)
    #         customer.register()
    #         # return redirect('store')
    #         return redirect('index')
    #     else:
    #         data = {
    #          'error': error_message,
    #          'value':value
    #         }
    #         return render(request, 'registration.html', data)


class OrderView(View):
    @method_decorator(auth_middleware)
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        orders = orders.reverse()
        return render(request, 'orders.html', {'orders':orders})

        

def logout(request):
    request.session.clear()
    return redirect('index')


class Paymentcomplete(View):
    def get(self, request):
        return render(request, 'complete.html')
        
    def post(self, request):
        
        body = json.loads(request.body)
        print('body =' ,body)
        customer = body.get('customer')
        price = body.get('price')
        orderlist = body.get('orderlist')
        transactionid ="xxxxxxxxxxxxxxxxx"
        orderplace = Orderplaced(customer=Customer(id=customer),
                        orderIds=orderlist,
                        price=price,
                        transactionid=transactionid,
                        )

        orderplace.ordersave()
        # print(customer,price,orderlist,order)

        return render(request, 'complete.html')
        

def checkout(request):
    if request.method == "POST":
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        payamount= request.POST.get('payamount')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products ,payamount)
        error_message = None
        value = {
            'address': address,
            'pincode': pincode

        }
        orderlist = []       
        for product in products:
        
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id = customer),
                            product=product,
                            price=product.price,
                            address=address,
                            phone = phone,
                            pincode = pincode,
                            quantity=cart.get(str(product.id))
                            )
            order.placeOrder()
            orderlist.append(order.id)

        orderlst =','.join([str(elem) for elem in orderlist])
        
            
        request.session['cart'] = {}

        print (orderlst)
        
        return render(request, 'payment.html', {'payment': payamount, 'orderlist': orderlst, 'customer':customer})


def test(request):

    user = authenticate(username='Christin', password='password')
    
    if user:
        value = True
    else:
        value = False
    return HttpResponse(value)



def search(request):
    search = request.GET.get("ser_itm")
    print("SEARCHITEM:", search)
    if Product.objects.filter(name__contains=search):
        itm=Product.objects.filter(name__contains=search)  
        html_data=render_to_string('text.html',{'products':itm},request=request)
        print("html_data")
        return JsonResponse({'html_data':html_data})
    else:
        return JsonResponse("Item not found", safe=False)