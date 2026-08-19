from django.shortcuts import render,redirect
from .models import *
import qrcode
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import re
from django.template.loader import render_to_string
from django.core.mail import send_mail

# Create your views here.

def index(request):
    category=Category.objects.all()
    cateid=request.GET.get('category')
    #print(cateid)
    #print(type(cateid)

    if cateid == 'all':
        momo=Momo.objects.filter(is_available=True)

    elif cateid:

        momo=Momo.objects.filter(is_available=True,category=cateid)
    else:
        momo=Momo.objects.filter(is_available=True)
    if request.method=='POST':
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        message=request.POST['message']
        Form.objects.create(name=name,email=email,phone=phone,message=message)

        # send mail
        subject = "Welcome to Our Website"
        message =''
        from_email="magar.yuchi@gmail.com"
        recipient_list =[email]
        send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list,html_message=render_to_string('core/email.html',{'username':name}))

        
        response= redirect('index')
        response.set_cookie('name',name,max_age=3600)
        return response
    
    context={
        'category':category,
        "momo":momo
    }
    return render(request,"core/index.html",context)

def about(request):
    return render(request,"core/about.html")
def contact(request):
    return render(request,"core/contact.html")

@login_required(login_url='log_in')
def menu(request):
    category= Category.objects.all()
    qr=qrcode.make("http://127.0.0.1:8000/menu/")
    qr.save("core/static/images/qr.png")

    context={
        'category':category
    }
    return render(request,"core/menu.html",context)
def service(request):
    return render(request,"core/services.html")
def testemonial(request):
    momo=Momo.objects.all()
    review=Review.objects.all()


    if request.method=='POST':
            name=request.POST['name']
            message=request.POST['message']
            rating=request.POST['rating']
            order=request.POST.get('order')

            Review.objects.create(name=name,message=message,rating=rating,order=order)
    context={
        'momo':momo,
        'review':review
    }

    return render(request,"core/testemonial.html",context)
def terms(request):
    return render(request,"core/terms.html")

'''
====================================================
                    AuthPart
====================================================
'''
def register(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']

        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.error(request,"username is already exists")
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.error(request,"email is already exists")
                return redirect('register')

            if not re.search(r"[A-Z]",password):
                messages.error(request,"password must contain at least one upper case")
                return redirect('register')
            if not re.search(r"\d",password):
                messages.error(request,"password must contain at least one digit")
                return redirect('register')
            
            try:
                user=User(first_name=fname,username=username)
                validate_password(password,user=user)  
                User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                return redirect('register')
            except ValidationError as e:
                for i in e.messages:
                    messages.error(request,i)
                    return redirect("register") 
        else:
            messages.error(request,"password and confirm password doesnot matched")
            return redirect('register')
        
    return render(request,"auth/register.html")

def log_in(request):
    name=request.COOKIES.get('name')
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        remember_me=request.POST.get("remember_me")

        if not User.objects.filter(username=username).exists():
            messages.error(request,"username is not register yet")
            return redirect("log_in")

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            if remember_me:
                request.session.set_expiry(36000)
            else:
                request.session.set_expiry(0)
            next=request.POST.get('next',"")
            return redirect(next if next else 'index')
        else:
            messages.error(request,'Invalid Password')
            return redirect('register')
        
    next=request.GET.get('next',"")

    return render(request,"auth/login.html",{'next':next,"name":name})

def log_out(request):
    logout(request)
    return redirect('log_in')    

# password change ------>
@login_required(login_url="log_in")
def password_change(request):
    form=PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form=PasswordChangeForm(user=request.user,data = request.POST)
        if form.is_valid():
            form.save()
        return redirect("log_in")
    return render(request,'auth/password_change.html',{'form':form})