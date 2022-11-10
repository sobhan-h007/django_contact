from re import template
from django.urls import path
from . import views
from django.conf.urls import handler404, handler500
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('contact', views.index, name='index'),  # this changed to create login from
    path('add-contact/', views.addContact, name='add-contact'),
    path('profile/<str:pk>/', views.contactProfile, name='profile'),
    path('edit-contact/<str:pk>/', views.editContact, name='edit-contact'),
    path('delete/<str:pk>/', views.deleteContact, name='delete'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change_password/', views.PasswordChangeView, name='change_password'),
    path('register/', views.register_user, name='register_user'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='recovery/reset_password.html'),name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='recovery/email_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="recovery/reset.html"),name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="recovery/success.html"), name='password_reset_complete'),

]

handler404 = 'contactlist.views.error_404_view'
handler500 = 'contactlist.views.error_500'
