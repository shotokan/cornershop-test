from django.urls import path

from . import views

app_name = "menu"

urlpatterns = [
    # path("<uuid:menu_id>", views.menu_view, name="select"),
    path("create/", views.MenuCreaterView.as_view(), name="create_new"),
    path("list/", views.MenuListView.as_view(), name="list_menus"),
    path("<int:pk>/update", views.MenuUpdate.as_view(), name="update_menu"),
    path("<uuid:menu_id>", views.menu_order, name="select"),
    path("orders/", views.OrdersRequestedListView.as_view(), name="orders_requested"),
    path("reminder/", views.send_reminder, name="reminder"),
]
