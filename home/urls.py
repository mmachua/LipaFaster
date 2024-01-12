from django.conf.urls import url
from django.urls import include, re_path, path

from home import views 
from home.views import HomeView
from home.views import stk_push_callback 

from . import views 

app_name = 'home'


urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    path('stk-push-callback/', views.stk_push_callback, name='stk_push_callback'),
    re_path('daraja/stk-push', views.stk_push_callback, name='mpesa_stk_push_callback'),

    #path('', views.home, name='home'),
    # path('merchant/create/', views.MerchantCreateView.as_view(), name='merchant_create'),
    # path('merchant/<int:pk>/update/', views.MerchantUpdateView.as_view(), name='merchant_update'),
    # path('paybill/create/', views.PaybillCreateView.as_view(), name='paybill_create'),
    # path('paybill/<int:pk>/update/', views.PaybillUpdateView.as_view(), name='paybill_update'),
    # path('qr/<int:pk>/', views.qr_code, name='qr_code'),
  
]

