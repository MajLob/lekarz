from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User


rooms = [
    {'id': 1, 'name': 'Zdrowie psychiczne'},
    {'id': 2, 'name': 'Jak znaleźć terapeutę'},
]


def home(request):
    context = {'rooms': rooms}
    return render(request, 'home.html', context)


def zaloguj(request):
    page = 'zaloguj'
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user=authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else: 
                messages.info(request, 'login lub hasło jest niepoprawne')
            
    context={'page':page}
    return render(request, 'base/zaloguj.html',context)

def rejestracja(request):
    return render(request, 'base/rejestracja.html')
 
@login_required(login_url='/zaloguj')
def mojekonto(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    context={'user':user, 'rooms':rooms}
    return render(request, 'base/mojekonto.html', context)

@login_required(login_url='/zaloguj')
def umow_wizyte(request):
    return render(request, 'base/umowwizyte.html')

def kontakt(request):
    return render(request, 'base/kontakt.html')

def wszyscypsycholodzy(request):
    return render(request, 'base/wszyscypsycholodzy.html')

@login_required(login_url='/zaloguj')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect ('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)

def rejestracjapsycholog(request):
    page = 'rejestracjapsycholog'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            zaloguj(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Błąd w czasie rejestracji')

    context = {'form':form}
    return render(request, 'base/rejestracjapsycholog.html', context)

def rejestracjaklient(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                user.username = user.username.lower()
                user.save()
                messages.success(request, "Rejestracja zakończona" + user)
                
                return redirect('zaloguj')
        
    context = {'form':form}
    return render(request, 'base/rejestracjaklient.html', context)

def wyloguj(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/zaloguj')
def mojekontopsycholog(request):
    return render(request,'base/mojekontolekarz.html' )

@login_required(login_url='/zaloguj')
def cennik(request):
    return render(request, 'base/cennik.html')

@login_required(login_url='/zaloguj')
def forum(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_messages': room_messages}
    return render(request, 'base/forum.html', context)

@login_required(login_url='/zaloguj')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host = request.user, 
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        # form = RoomForm(request.POST) 
        # if form.is_valid():
            # room = form.save(commit=False)
            # room.host = request.user
            # room.save()
            # return redirect('home')
    context={'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/zaloguj')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/zaloguj')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.user:
        return HttpResponse("Brak dostępu")
    if request.method == 'POST':
        room.delete()
        return redirect('/forum/')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('/forum/')
    return render(request, 'base/delete.html', {'obj': message})
