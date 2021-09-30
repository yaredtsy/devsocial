from django.urls import path
from .views import project,projects,createProject,updateProject,deleteProject

urlpatterns = [
    path('',projects,name="projects"),
    path('projects/<str:pk>',project,name="project"),

    path('create-project/',createProject,name='create-project'),
    path('update-project/<str:pk>/',updateProject,name='update-project'),

    path('delete-project/<str:pk>/',deleteProject,name='delete-project'),
]
