from django.shortcuts import render, redirect
from myCrm.forms import LoginForm, AddRecordForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    users = User.objects.all()
    context = {"users": users}
    return render(request, "myCrm/home.html", context)


def signIn(request):
    if request.user.is_authenticated == True:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user != None:
            login(request, user=user)
            return redirect("home")
    
    loginForm = LoginForm()
    context = {"form": loginForm, "page": "signIn"}

    return render(request, "myCrm/register.html",context)


def logOut(request):
    logout(request)
    return redirect("signIn")


def signUp(request):
    registerForm = UserCreationForm()
    if request.method == "POST":
        registerForm = UserCreationForm(request.POST)
        if registerForm.is_valid:
            registerForm.save()
            return redirect("home")
        else:
            HttpResponseServerError
    context = {"form": registerForm, "page": "signUp"}
    return render(request, 'myCrm/register.html', context)


def addRecord(request):
    userForm = AddRecordForm()
    if request.method == "POST":
        userForm = AddRecordForm(request.POST)
        if userForm.is_valid:
            userForm.save()
            username = request.POST.get("username")
            messages.success(request, f"{username} added successfully!")
            return redirect("add_record")
        else:
            HttpResponseServerError
    context = {"form": userForm}
    return render(request, 'myCrm/add_record.html', context)


def update(request, pk):
    user = User.objects.get(id=pk)
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        if request.POST.get("submit") == "Save":
            print(username)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, f"{user.username} updated successfully!")
            return redirect("home")
        else:
            user.delete()
            messages.success(request, f"{user.username} deleted successfully!")
            return redirect("home")
    userForm = AddRecordForm(instance=user)
    context = {"form": userForm, "page": "edit"}
    return render(request, "myCrm/add_record.html", context)



