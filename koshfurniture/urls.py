from django.urls import path ,include
from . import views
from .views import Login , Index,Store,Cart,OrderView,Signup,Paymentcomplete
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings
from django.utils.decorators import method_decorator
from .middlewares.auth import auth_middleware


urlpatterns = [
    path('', Index.as_view(), name="index"),
    # path('contact/', views.contact, name="contact"),
    path('store/', Store.as_view() , name="store"),
    path('cart/', Cart.as_view(), name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('login/', Login.as_view(), name="login"),
    path('signup/', Signup.as_view(), name="signup"),
    path('logout/', views.logout, name="logout"),
    path('order/', auth_middleware(OrderView.as_view()), name="order"),
    path('complete/' ,Paymentcomplete.as_view(), name="complete"),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
