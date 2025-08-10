from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_password, name='generate_password'),
    path('history/', views.password_history, name='password_history'),
    path('toggle-favorite/<int:password_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('delete/<int:password_id>/', views.delete_password, name='delete_password'),
    path('generate-qr/<int:password_id>/', views.generate_qr_code, name='generate_qr'),
    path('scan-qr/<int:password_id>/', views.scan_qr_code, name='scan_qr'),
]
