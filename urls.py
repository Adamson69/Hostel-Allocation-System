from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),

    path("dashboard/", views.student_dashboard, name="student_dashboard"),
    path("apply/", views.apply_view, name="apply"),
    path("admin-panel/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-panel/allocate/<int:app_id>/", views.allocate_view, name="allocate"),
]
