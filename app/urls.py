from django.urls import path,include
from .import views
urlpatterns = [

    path('', views.index, name='index'),
    path('index/', views.index, name='index'),

    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('userhome/', views.userhome, name='userhome'),
    path('workshopregister/', views.workshopregister, name='workshopregister'),


    path('success/', views.success, name='success'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('users/', views.user_list, name='user_list'),
        path('about/', views.about, name='about'),

    path('login/', views.login, name='login'),
        path('wlogin/', views.wlogin, name='wlogin'),

    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),  
    path('workshoplist/', views.workshoplist, name='workshoplist'),  
    path('register_vehicle/', views.register_vehicle, name='register_vehicle'), 
    path('yourvehicles/', views.yourvehicles, name='yourvehicles'), 
    path("book/<int:id>/", views.book_service, name="book"),
    path('mybookings/', views.mybookings, name='mybookings'),
    path('servicerequestpage/', views.servicerequestpage, name='servicerequestpage'),
    path('update-booking/<int:booking_id>/<str:status>/',
     views.update_booking_status,
     name='update_booking_status'),
     path("pay/<int:booking_id>/", views.make_payment, name="make_payment"),
  path("payment-success/", views.payment_success, name="payment_success")


    # path('logout/', views.logout_view, name='logout'),

    



    ]