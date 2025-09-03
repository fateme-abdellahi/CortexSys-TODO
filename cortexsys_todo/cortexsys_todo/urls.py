"""
URL configuration for cortexsys_todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.views import RegisterView
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #auth
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),

    #CRUD   
    path('api/tasks/', views.TasksListCreateView.as_view(), name='list_create_tasks'),
    path('api/tasks/<int:pk>/', views.TaskUpdateDeleteView.as_view(), name='update_delete_tasks'),
]
