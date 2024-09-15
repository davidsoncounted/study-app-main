from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import Roomform, UserForm, Myusercreationform
# Create your views here.

# rooms = [
#         {'name': 'Onyeka', 'details': 'we want to learn'},
#         {'name': 'Arinze', 'details': 'we want to learn data science'},  
#         {'name' : 'davidson', 'details': 'we want to learn python'},
#     ]
def register(request):
    form = Myusercreationform()

    if request.method == 'POST':
        form = Myusercreationform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            # user.email = user.email.lower()
            user.save() 
            login(request, user)
            return redirect('/') 
        else:
            messages.error(request, 'something went wrong with the registration ')
            return redirect('register')
    context = {'forms': form}
    return render(request, 'register.html', context )

    # if request.method == 'POST':
    #     username = request.POST['username']
    #     email = request.POST['email']
    #     password = request.POST['password']
    #     repeat_password = request.POST['repeat-password']

    #     if repeat_password == password:

    #         if User.objects.filter(username = username).exists():
    #             messages.info(request, 'these username already exists')
    #             return redirect('login')
            
    #         elif User.objects.filter(email = email).exists():
    #             messages.info(request, 'these email already exists')
    #             return redirect('login')
            
    #         else:
    #             user = User.objects.create_user(username=username, email=email, password=password, repeat_password= repeat_password)
    #             user.save()
    #             return redirect('login')
            
    #     else:
    #         messages.info(request, 'the password do not match')
    #         return redirect('register')
        
    # return render(request, 'register.html')
   


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            username = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist')

        user = authenticate(request, username=username, password=password)
  
        if user is not None:
            login(request, user)
            return redirect('/')
        
        else:
            messages.error(request, 'username or password does not exist')
    

    return render(request, 'login.html')



def logoutPage(request):
    logout(request)
    return redirect('/')


def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains= q)|
        Q(name__icontains= q)|
        Q(description__icontains= q)
        )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')



    contents = {'contents': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'home.html', contents)

def room(request, pk):
    room = Room.objects.get(name=pk) 
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
       
        room.participants.add(request.user)

        return redirect('room', pk=room)

    contents = {'contents': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'room.html',contents)  



def userProfile(request, pk):
    
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'contents': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'profile.html', context)



@login_required(login_url='login')
def createRoom(request):
    topics = Topic.objects.all()
    form = Roomform()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name= topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        # form = Roomform(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('/')

    context = {'form': form, 'topics': topics}
    return render(request, 'room-form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('you are not allowed dhere!!+')

    form = Roomform(instance = room)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name= topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        # form = Roomform(request.POST, instance= room)
        # if form.is_valid():
        #     form.save()
        return redirect('/')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'room-form.html', context)



@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('/')
    return render(request, 'delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):

    message = Message.objects.get(id=pk)
    # participants = Room.participants.all()
    if request.method == 'POST':
        message.delete()
        
        # message.participants.remove(request.user)

        return redirect('room')
    context = {'obj': message,}
    return render(request, 'delete.html', context)

@login_required(login_url='login')
def deleteRecent(request, pk):

    message = Message.objects.get(id=pk)
    # participants = Room.participants.all()
    if request.method == 'POST':
        message.delete()
        
        # message.participants.remove(request.user)

        return redirect('/')
    context = {'obj': message,}
    return render(request, 'delete.html', context)


@login_required(login_url= 'login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
     

    return render(request, 'update-user.html', {'form': form})



def topicPage(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)


    return render(request, 'topics.html', {'topics':topics})


def activityPage(request):

    room_message = Message.objects.all()

    return render(request, 'activity.html', {'room_message': room_message})