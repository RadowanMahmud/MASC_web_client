"""MascWebCore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include  # add this
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("modules.home.urls")),
    path('labs/',include("modules.MascLab.urls")),
    path('engine/',include("modules.MascEngine.urls")),
    path('auth/',include("modules.UserAuthentication.urls")),
    path('profile/',include("modules.UserProfile.urls")),
    path('properties/', include("modules.CipherManager.urls")),
    path('plugins/', include("modules.plugins.urls"))
]
