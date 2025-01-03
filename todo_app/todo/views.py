from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from todo import models
from todo.models import TODO
# Create your views here.

def signup(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('pwd')
        confirm_password=request.POST.get('confirmpwd')
        if password==confirm_password:
            print(username,email,password)
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            return redirect('/login')
        else:
            template=loader.get_template('signup.html')
            error={
                'context':'Your password and comfirm password are not matched!! Please try again'
            }
            return HttpResponse(template.render(error,request))
    else:
        return render(request, 'signup.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pwd=request.POST.get('pwd')
        user=authenticate(username=username,password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/todopage')
        else:
            error={
                'context':'User name doesnt exit!! Please Signup first '

            }
            return render(request,'login.html',error)
    return render(request,'login.html')
def get_todo(request):

    if request.method=='POST':
        title=request.POST.get('title')
        obj=models.TODO(title=title,user=request.user)
        obj.save()
        result=models.TODO.objects.filter(user=request.user).order_by('date')
        return render(request,'todopage.html',{'res':result})
    else:
        result=models.TODO.objects.filter(user=request.user).order_by('date')
        return render(request, 'todopage.html',{'res':result})

def edittodo(request,srno):

    if request.method=='POST':
        title=request.POST.get('title')
        obj=models.TODO.objects.get(srno=srno)
        obj.title=title
        obj.save()
        result=models.TODO.objects.filter(user=request.user)
        return redirect('/todopage',{'res':result})
    else:
        obj = models.TODO.objects.get(srno=srno)
        return render(request, 'edittodo.html', {'obj': obj})

def deletetodo(request,srno):
    obj=models.TODO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')
def signout(request):
    logout(request)
    return redirect('/login')
