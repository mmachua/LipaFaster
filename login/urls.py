from django.conf.urls import url
from django.urls import include, re_path
from django.urls import include ,path
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import (
    login,
    logout,
#     password_reset_confirm,
#      password_reset,
#     password_reset_done,
#     password_reset_complete
     )
from django.contrib.auth.views import(
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
#from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from . import views as myapp_views ,views
from login.views import SignUpView, logout

app_name = 'login'

urlpatterns = [
    
    #sign in form
    re_path(
        'login/',
        auth_views.LoginView.as_view(template_name='login/accounts.html'),name='login',
    ),
    re_path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='login/logout.html'),name='logout',
    ),
    re_path( r'^register/$',SignUpView.as_view(template_name="login/reg_form.html"),name='register'),
    
    re_path(r'^profile/$', views.view_profile, name='view_profile'),
    re_path(r'^profile/(?P<pk>\d+)/$', views.view_profile, name='view_profile_with_pk'),
    re_path(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    re_path(r'^change-password/$', views.change_password, name='change_password'),

    
    re_path(r'^reset-password/$',auth_views.PasswordResetView.as_view(),{'template_name':
        'login/reset_password.html','post_reset_redirect':
        'login:password_reset_done','email_template_name':
        'login:reset_password_email.html' },name="reset_password"),

    #path(r'^reset-password/done/$',PasswordResetDoneView.as_view(),name="password_reset_done"),
    re_path(r'^reset-password/done/$', auth_views.PasswordResetDoneView.as_view(template_name='login/password_reset_done.html'),
     name='password_reset_done'),
    #path(r'^reset-password/confirm/$',PasswordResetConfirmView.as_view() , name='password_reset_confirm'),
    re_path(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    auth_views.PasswordResetConfirmView.as_view(),{'template_name':'login/reset_password_confirm.html'},
    name='password_reset_confirm'),
    
    re_path(r'^reset-password/done/$', auth_views.PasswordResetCompleteView.as_view, 
    {'template_name':'login/reset_password_done.html'},
     name='password_reset_done'),



]