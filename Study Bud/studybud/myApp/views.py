from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Message, Topic
from .forms import TopicForm, RoomForm, LogInForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# rooms = [
#     {"id": 1, "name": "Let's Learn Python"},
#     {"id": 2, "name": "Mobile Apps Dev"},
#     {"id": 3, "name": "Web Apps Dev"}
# ]
def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')
    
    form = LogInForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "incorrect username or password")
    context = {'form': form, 'page': page}
    return render(request, "myApp/login_register.html", context)


def registerPage(request):
    page = "register"
    passwdconf = ""
    form = UserCreationForm()
    if request.method == 'POST':
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        if confirmpassword != password:
            passwdconf = "failed"
            context = {'form': form, 'page':page, 'passwdconf': passwdconf}
            return render(request, 'myApp/login_register.html', context)
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save()
            login(request, user)
        return redirect('home')
    
    context = {'form': form, 'page': page}
    return render(request, 'myApp/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def userProfile(request, pk):
    user = User.objects.get(pk = pk)
    rooms = user.room_set.all()
    comments = user.message_set.all()
    topics = Topic.objects.all()
    page = "profile"
    context = {'user': user, 'rooms': rooms, 'comments': comments, 'topics': topics, "page": page}
    return render(request, "myApp/profile.html", context)


def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk = user.id)
    return render(request, "myApp/update-user.html",{'form': form})


def home(request):
    topics = Topic.objects.all()[:5]
    page = "home"
    #we need to get the rooms depending on the topic, name, host username qeuery passed to us via the GET method
    #if no parameter was passed we return all the rooms
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(host__username__icontains = q)
        )
    roomcount = rooms.count()
    comments = Message.objects.all().order_by('-created').filter(
        Q(room__name__icontains = q) |
        Q(room__topic__name__icontains = q)
    )
    context = {"rooms": rooms, "topics": topics, "roomcount": roomcount, "comments": comments, "page": page}
    return render(request, 'myApp/home.html', context)


def room(request, pk):
    room  = Room.objects.get(pk= int(pk))
    #go to the message model and fetch the set of all messages related to me
    room_messages = room.message_set.all() #or the old fationed way
    #room_messages = Message.objects.filter(room = room)
    participants = room.participants.all()
    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, "myApp/room.html", context)


def createComment(request):
    message_body = request.POST.get('body')
    room_id = request.POST.get('room_id')
    room = Room.objects.get(id = room_id)
    curr_user = request.user
    #the user is added to the list of participants when he adds his chart/message
    room.participants.add(curr_user)
    Message.objects.create(user = curr_user, room = room, body = message_body)
    return redirect('room', pk= room.id)


def deleteComment(request, pk):
    comment =  Message.objects.get(id = pk)
    room_id = comment.room.id
    page = request.GET.get('page')
    if request.method == 'POST':
        comment.delete()
        if page == "home":
            return redirect('home')
        return redirect('room', pk = room_id)
    return render(request, "myApp/delete.html", {'obj': comment, 'page': page})


@login_required(login_url="login")
def createRoom(request):
    topics = Topic.objects.all()
    form = RoomForm()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host = request.user,
            name = request.POST.get('name'),
            topic = topic,
            description = request.POST.get('description')
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, "myApp/create-room.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id = int(pk))
    #the instance attribute initializes the form with the values of the room attributes/variable
    form = RoomForm(instance=room)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, "myApp/create-room.html", context)


login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    page = "home"
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, "myApp/delete.html", {'obj': room, 'page': page})


def topicsPage(request):
    topics = Topic.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    topics = Topic.objects.filter(
        name__icontains = q
    )

    return render(request, "myApp/topics.html",{"topics": topics})


def activitiesPage(request):
    comments = Message.objects.all()
    return render(request, "myApp/activity.html", {"comments": comments})


