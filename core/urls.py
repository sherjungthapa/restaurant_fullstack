from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *
urlpatterns = [
    path("",index,name="index"),
    path("about/",about,name="about"),
    path("menu/",menu,name="menu"),
    path("service/",service,name="service"),
    path("testemonial/",testemonial,name="testemonial"),
    path("contact/",contact,name="contact"),
    path("terms/",terms,name="terms"),
   
      
    #   auth part--------------------->
    path("log_in/",log_in,name='log_in'),
    path("register/",register,name='register'),
    path("logout/",log_out,name='log_out'),
    path("password_change/",password_change,name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html',html_email_template_name='auth/email.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

