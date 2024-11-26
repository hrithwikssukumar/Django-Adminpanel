
from django.urls import path
from.import views 

urlpatterns = [
    path('',views.home,name = 'home'),
    path('register/',views.register,name = 'register'),
    path('login/',views.user_login,name = 'userlogin'),
    path('dashboard/',views.dashboard,name = 'dashboard'),
    path('logout/',views.user_logout,name = 'userlogout'),
    path('adminhome/',views.admin_home,name = 'adminhome'), 
    path('adminlogout/',views.admin_logout,name = 'adminlogout'), 
    path('useradd/',views.user_add,name = 'useradd'),
    path('delete-user/<int:user_id>/', views.delete_user, name='deleteuser'), 
    path('edit/<int:user_id>/', views.edit, name='edit'),
    path('search',views.user_search,name='search')
]
