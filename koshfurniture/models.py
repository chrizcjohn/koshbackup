from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Category(models.Model):
    name = models.TextField(max_length=200, null=True)
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.TextField(max_length=200, null=True)
    
    def __str__(self):
        return self.name



class Discount(models.Model):
    discount = models.TextField(max_length=200, null=True)

    def __str__(self):
        return self.discount

class Material(models.Model):
    material_name = models.TextField(max_length=200, null=True)
    
    def __str__(self):
        return self.material_name

class Customer(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.TextField(max_length=200, null=True)
    email = models.TextField(max_length=200, null=True)
    password = models.TextField(max_length=200, null=True)
    phone = models.BigIntegerField (null=True)

    def register(self):
        self.save()

    def isExists(self):
        if Customer.objects.filter(email=self.email):
           return True
        return False
           
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

        
    # def __str__(self):
    #     return self.name

class Product(models.Model):
    name = models.TextField(max_length=200, null=True)
    price = models.BigIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    Description = models.TextField(max_length=200, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL , null=True ,blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL , null=True ,blank=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL , null=True ,blank=True)
    image = models.ImageField(null=True, blank=True)
    
    
    
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids )


    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_id(category_id):
        if category_id: 
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True)
    quantity = models.BigIntegerField(default=1)
    price = models.BigIntegerField(default=0)
    address = models.TextField(max_length=200, default='', blank=True)
    pincode = models.TextField(max_length=200, default='')
    phone = models.BigIntegerField(default=0, blank =True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer = customer_id).order_by('-date')


    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.BigIntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True , blank = True)
    address = models.TextField(max_length=200, null=True)
    city = models.TextField(max_length=200, null=True)
    state = models.TextField(max_length=200, null=True)
    pincode = models.TextField(max_length=200, null=True)
    phone = models.TextField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Orderplaced(models.Model):
    price = models.BigIntegerField(default=0)
    orderIds = models.TextField(max_length=200,default ='')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    transactionid = models.TextField(max_length=200, null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def ordersave(self):
        return self.save()
    
    

