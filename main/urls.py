from django.urls import path
from main import views

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("search/", views.search, name="search"),
    path("chart/<str:chartType>/", views.chartGet, name="chart"),
    path("students/<int:student>/", views.get_student, name="student"),
    path("groups/<int:group>/", views.get_group, name="group"),
    path("parents/<int:parent>/", views.get_parent, name="parent")
]
