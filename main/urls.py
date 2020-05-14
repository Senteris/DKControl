from django.urls import path
from main import views

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("search/", views.search, name="search"),
    path("chart/<str:chartType>/", views.chartGet, name="chart")
]
