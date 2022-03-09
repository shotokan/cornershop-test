from django.urls import path

from . import views

app_name = "staff"

urlpatterns = [
    path("menu/<uuid:menu_id>", views.CreateOrderView.as_view(), name="select"),
    path("orders/", views.ListOrdersByStaffView.as_view(), name="list_orders_staff"),
]
