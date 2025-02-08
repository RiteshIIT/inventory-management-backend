"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from login.views import LoginApi
from login.views import InventoryPage
from login.views import NewProduct
from login.views import ProductDetail
from login.views import LogoutApi


urlpatterns = [
    path('admin/', admin.site.urls),

    
    path('login/', LoginApi.as_view(), name='login'),
    path('logout/', LogoutApi.as_view(), name='logout'),

    
    path('inventory/', InventoryPage.as_view(), name='inventory'),
    path('inventory/new/', NewProduct.as_view(), name='new_product'),
    path('inventory/<int:pk>/', ProductDetail.as_view(), name='product_detail'),

    
    path('api/', include('login.urls')),
    path('api/auth/', include('login.urls'))
]


