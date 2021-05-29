from . import views
from django.urls import path

urlpatterns=[
  path('register/',views.register,name='register'),
  path('login/',views.login,name='login'),
  path('logout/',views.logout,name='logout'),
  path('activate/<uidb64>/<token>/',views.activate, name='activate'),
  path('',views.dashboard,name='dashboard'),
  path('forgot/',views.forgot,name='forgot'),
  path('reset_validate/<uidb64>/<token>/',views.reset_validate,name='reset_validate'),
  path('reset/',views.reset,name='reset'),
]