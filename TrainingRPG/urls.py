"""TrainingRPG URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views  # Import Django's auth views

from RPG import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main'),  # Homepage
    path('login/', views.loginpage, name='login'),  # Login page
    path('signup/', views.signuppage, name='signup'),  # Signup page
    path('update_profile/', views.update_profile, name='update_profile'),  # Update profile page
    path('main/', views.main_page, name='main'),  # Main RPG page
    path('logout/', views.logoutpage, name='logout'),  # Logout
    path('inventory/', views.inventory_view, name='inventory'),
    path('shop/', views.shop, name='shop'),
    path('purchase/<int:item_id>/', views.purchase_item, name='purchase_item'),
    path('sell/<int:item_id>/', views.sell_item, name='sell_item'),
    path('battle/start/', views.start_battle, name='start_battle'),
    path('battle/', views.battle_simulator, name='battle'),  # Assuming you create a battle_simulator view
]
