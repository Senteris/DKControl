from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.shortcuts import render, redirect


def login(request):
    error = None
    if request.user.is_authenticated:
        return redirect('main')
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User '{}' is valid, active and authenticated".format(user.username))
                user_login(request, user)

                if request.GET.get('next', None) is not None:
                    return redirect(request.GET['next'])
                else:
                    return redirect('main')
            else:
                error = "  Имя или пароль неверны"
        else:
            # the authentication system was unable to verify the username and password
            error = "  Имя или пароль неверны"
    return render(request, "login.html", {'error': error})