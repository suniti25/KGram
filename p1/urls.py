"""p1 URL Configuration

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
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from .views import welcome_view

api_urls = [
    path('user/', include('user.urls')),
    path('post/', include('post.urls')),
]

urlpatterns = [
    path('', welcome_view),
    path('admin/', admin.site.urls),
    # apis
    path('api/', include(api_urls)),

    # documentation
    path('openapi/', get_schema_view(title='P1', description='API for P1', version='0.1.0'), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]
