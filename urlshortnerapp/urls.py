
"""
URL configuration for urlshortner_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from . import views

urlpatterns = [

    path('',views.signup,name='signup'),
    path('login-page/',views.login_fn,name='login'),
    path('create-page/',views.create_fn,name='create'),
    path('<str:rand_char>',views.redirect_to_original,name='redirect'),
    path('list-page/',views.list_fn,name='list'),
    path('edit-page/<int:pk>/',views.edit_fn,name='edit'),
    path('delete-page/<int:pk>/',views.delete_fn,name='delete'),
    path('logout-page/',views.logout_fn,name='logout'),
    path('search/',views.search_fn,name='search')

]