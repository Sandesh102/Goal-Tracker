from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('home/',homepage,name='homepage'),  
    path('task/', task, name='task'),      
    path('delete/<int:id>/', delete, name='delete'),  
    path('update/<int:id>/', update, name='update'),  
    path('completed/<int:id>/', completed, name='completed'),  
    path('incompleted/<int:id>/',incompleted,name='incompleted'),
    path('login/',login_page,name="login_page"),
    path('register/',register_page,name="register_page"),
    path('logout/',logout_page,name="logout_page"),
    
]
