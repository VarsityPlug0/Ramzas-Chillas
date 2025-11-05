from django.urls import path
from . import views

urlpatterns = [
    path('create-order-whatsapp/', views.create_order_and_redirect_whatsapp, name='create_order_whatsapp'),
    path('<str:order_id>/status/', views.get_order_status, name='get_order_status'),
    path('', views.list_orders, name='list_orders'),
    path('<int:order_id>/update-status/', views.update_order_status_api, name='update_order_status_api'),
]