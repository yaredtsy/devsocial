from project import forms

from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate, logout

from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from .forms import CustomeuserCreationForm,ProfileForm,SkillForm,MessageForm

from django.contrib.auth.decorators import login_required

from .models import Profile, Skill,Message
from django.db.models import Q

from .utils import searcProfiles,paginateProfile

def loginUser(request):
    
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Username does not exist")

        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('profiles')
        
        else:
            messages.error(request,'Username Or password is incorrect')
    
    page ="login"
    context = {"page":page}

    return render(request,'users/login_register.html',context)

def logoutUser(request):

    logout(request)
    return redirect('login')

def registerUser(request):

    form = CustomeuserCreationForm()
    if request.method == 'POST':
        form = CustomeuserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,"user account was created!")
    
            login(request,user)
            return redirect('edit-account')

        else:
            messages.error(request,'An error has occured during registration')

 
    page='register'

    context={'page':page,'form':form}

    return render(request,'users/login_register.html',context)

def profiles(request):
    profiles,search_query = searcProfiles(request)
    custom_range,profiles = paginateProfile(request,profiles,2)

    context = {'profiles':profiles,'custom_range':custom_range,'profiles':profiles,'search_query':search_query}

    return render(request,'users/profile.html',context)

def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)

    topskills= profile.skill_set.exclude(descriprion__iexact="")

    otherskills = profile.skill_set.filter(descriprion="")
    projects = profile.project_set.all()

    context = {
        'profile':profile,
        'otherskills':otherskills,
        'topskills':topskills,
        'projects':projects
        }


    return render(request,'users/user-profile.html',context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skill = profile.skill_set.all()

    projects = profile.project_set.all()

    context = {
        'profile':profile,
        'skills':skill,
        
        'projects':projects
        }
        
    return render(request,'users/account.html',context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()

            return redirect('user-account')

    context = {"form":form}
    return render(request,'users/profile_form.html',context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,"Skill was added Successfully")
            return redirect('user-account')
          
    context = {"form":form}
    return render(request,'users/skill_form.html',context)



@login_required(login_url='login')
def updateSkill(request,pk):

    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            skill.save()
            messages.success(request,"Skill was added Successfully")
            return redirect('user-account')
          
    context = {"form":form}
    return render(request,'users/skill_form.html',context)

@login_required(login_url='login')
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        return redirect('user-account')

    context = {"object":skill}
    return render(request,"delete_objects.html",context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context={'messageRequests':messageRequests,'unreadCount':unreadCount }
    return render(request,'users\inbox.html',context)

@login_required(login_url='login')
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {'message':message}

    return render(request,'users\message.html',context)

def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            messages.sender = sender
            messages.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
        
            messages.success(request,"Your message was successfuly sent ")
            
            return redirect('user-profile',pk=recipient.id)

    context = {'recipient':recipient,"form":form}

    return render(request,'users/message_form.html',context)