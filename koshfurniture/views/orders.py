from django.views import View
from django.shortcuts import render, redirect
from KoshFurnishing.koshfurniture.models import *

class order(View):
    def get(self,request):
        auth_middleware()
        if request.method == "GET":
            customer = request.session.get('customer')
            orders = Order.get_orders_by_customer(customer)
            print(orders)
            orders = orders.reverse()
            return render(request, 'orders.html', {'orders':orders})
