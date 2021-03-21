from django.urls import path ,include
from . import views
from .views import Login , Index,Store,Cart,OrderView,Signup,Paymentcomplete
from django.contrib import admin
from django.contrib.auth import views as auth_views

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
    path('complete/', Paymentcomplete.as_view(), name="complete"),
    
    path('reset-password/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('reset-password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('test/', views.test ,name="test"),
    path('loginuser/', auth_views.LoginView.as_view(template_name="login.html")),
    path('store/search/',views.search,name="search")
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
