from django.http import HttpResponse, JsonResponse, request
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import conf
from proiect.models import Messages
import json



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def newUser(request):
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                saveUser = User.objects.create_user(request.POST.get('username'), password = request.POST.get('password1'))
                saveUser.save()
                return render(request, 'signup.html', {'form': UserCreationForm(), 'info': 'Userul ' + request.POST.get('username') + ' s-a bagat in treaba'})
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'Userul ' + request.POST.get('username') + ' exista'})
        else:
            return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'Parola incorecta'})
    
    else:
        return render(request, 'signup.html', {'form': UserCreationForm})

def loginUser(request):
    if request.method == "POST":
        loginSucces = authenticate(request, username = request.POST.get('username'), password = request.POST.get('password'))
        if loginSucces is None:
            return render(request, 'login.html', {'form': AuthenticationForm(), 'error': 'Username sau parola incorecta'})
        else:
            login(request, loginSucces)
            return redirect('userPage')
    else:
        return render(request, 'login.html', {'form': AuthenticationForm()})

def indexPage(request):
    return render(request, 'index.html')

def logoutPage(request):
    if request.method == "POST":
        logout(request)
        return redirect('loginUser')

def userPage(request):
    userList =User.objects.values()
    return render(request, 'userPage.html', {"userList": userList})

def joinRoom(request):
    sender = request.user.username
    receiver = request.POST['user']
    # print("sender" + sender)
    # print("receiver" +  receiver)
    return redirect('/'+receiver+'/?username='+sender)

def chatRoom(request, receiver):
    sender = request.user.username
    # receiver = request.GET['receiver']
    # print("receiver---->" +  receiver)
    # print("sender----->" + sender)
    sentMessages = getSentMessages(sender, receiver)
    receivedMessages = getReceivedMessages(sender, receiver)
    return render(request, 'chatRoom.html', {
        'receiver': receiver,
        'sender': request.user.username,
        'sentMessages': sentMessages,
        'receivedMessages': receivedMessages})

def send(request, receiver):    
    sender = request.user.username
    message = request.POST['message']
    print("receiver---->" +  receiver)
    print("sender----->" + sender)
    print("mesaj trimis ---->" + message)

    newMessage = Messages.objects.create(sender=sender, receiver=receiver, message=message)
    newMessage.save()

    sentMessages = getSentMessages(sender, receiver)
    receivedMessages = getReceivedMessages(sender, receiver)

    return render(request, 'chatRoom.html', {
        'receiver': receiver,
        'sender': request.user.username,
        'sentMessages': sentMessages,
        'receivedMessages': receivedMessages})


# interpreteaza din baza de date si returneaza un dictionar cu mesaje trimise si data
def getSentMessages(sender, receiver):

    # print("receiver---->" +  receiver)
    # print("sender----->" + sender)
    senders = Messages.objects.filter(sender=sender, receiver=receiver).values('sender')
    receivers = Messages.objects.filter(sender=sender, receiver=receiver).values('receiver')
    messages = Messages.objects.filter(sender=sender, receiver=receiver).values('message')
    dates = Messages.objects.filter(sender=sender, receiver=receiver).values('dateSent')
    print("TOATE MESAJELE TRIMISE ---->")
    print(senders)
    print(receivers)
    print(messages)
    # print(dates)
    messagesList = []
    datesList = []
    for message in messages:
        messagesList.append(message['message'])
    for date in dates:
        datesList.append(date['dateSent'].strftime("%m/%d/%Y, %H:%M:%S"))

    zipIterator = zip(messagesList, datesList)
    dataDictionarry = dict(zipIterator)
    print(json.dumps(dataDictionarry, sort_keys=False, indent=4))
    return dataDictionarry

# interpreteaza din baza de date si returneaza un dictionar cu mesaje primite si data
def getReceivedMessages(sender, receiver):
    messages = Messages.objects.filter(sender=receiver, receiver=sender).values('message')
    dates = Messages.objects.filter(sender=receiver, receiver=sender).values('dateSent')
    print("TOATE MESAJELE PRIMITE ---->")
    # print(messages)
    # print(dates)
    messagesList = []
    datesList = []
    for message in messages:
        messagesList.append(message['message'])
    for date in dates:
        datesList.append(date['dateSent'].strftime("%m/%d/%Y, %H:%M:%S"))

    zipIterator = zip(messagesList, datesList)
    dataDictionarry = dict(zipIterator)
    print(json.dumps(dataDictionarry, sort_keys=False, indent=4))
    return dataDictionarry

