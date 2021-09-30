from users.views import profiles
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project

from django.contrib.auth.decorators import login_required
from .utils import searcProject,paginateProjects
from django.contrib import messages

# Create your views here.

from .forms import ProjectForm,ReviewForm

def projects(request):
    projects,search_query = searcProject(request)
    custom_range,projects = paginateProjects(request,projects,6)

    context = {"projects":projects,'search_query':search_query,'custom_range':custom_range}

    return render(request,"projects/projects.html",context)

@login_required(login_url="login")
def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tag.all()
    form = ReviewForm()
    print(projectObj.reviewers)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getvoteCount
        
        return redirect('project',pk=projectObj.id)
        messages.success(request,"Your review was submited")

    context = {"project":projectObj,'tags':tags,'form':form}
    
    return render(request,"projects/single-projects.html",context)

@login_required(login_url="login")
def createProject(request):
    form = ProjectForm()
    profile = request.user.profile

    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            return redirect('projects')
    context = {'form':form}
    return render(request,"projects/project_form.html",context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form':form}
    return render(request,"projects/project_form.html",context)

@login_required(login_url="login")
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == "POST":
        project.delete()
        return redirect('projects')

    context = {"object":project}
    return render(request,"delete_objects.html",context)