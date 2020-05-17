from django.urls import path

from main.views.chartGet import chartGet
from main.views.get_group import get_group
from main.views.get_parent import get_parent
from main.views.get_session import get_session
from main.views.get_student import get_student
from main.views.logout import logout
from main.views.main import main
from main.views.login import login
from main.views.getUser import getUser
from main.views.search import search

urlpatterns = [
    path("", main, name="main"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("search/", search, name="search"),
    path("chart/<str:chartType>/", chartGet, name="chart"),
    path("students/<int:student>/", get_student, name="student"),
    path("groups/<int:group>/", get_group, name="group"),
    path("parents/<int:parent>/", get_parent, name="parent"),
    path("users/<int:user>/", getUser, name="user"),
    path("sessions/<int:session>/", get_session, name="session"),
]
