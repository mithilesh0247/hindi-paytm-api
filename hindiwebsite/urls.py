"""hindiwebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url,include
from django.urls import path
from testapp import views
from testapp.views import initiate_payment, callback
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('java/', views.java),
    path('python/', views.python),
    path('aptitude/', views.aptitude),
    path('logout/', views.logout),
    #path('signup/', views.signup),
    path('signup/', views.SignUpView.as_view()),
    path('accounts/',include('django.contrib.auth.urls')),
    path('pay/', initiate_payment),
    path('callback/', callback),
    
]
    
