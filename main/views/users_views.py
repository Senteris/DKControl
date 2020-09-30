from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout

from main.decorators import employee_required
from main.models import Parent, Student, User


@login_required(login_url="/login/")
def get_user(request, user):
    user_model = User.objects.get(id=user)
    if set_model(user_model, request):
        return redirect('user', user)
    return render(request, 'user.html', {"user": user_model})


@login_required(login_url="/login/")
def get_student(request, student):
    student_model = Student.objects.get(id=student)
    if set_model(student_model, request):
        return redirect('student', student)
    return render(request, 'student.html', {"student": student_model})


@login_required(login_url="/login/")
def get_parent(request, parent):
    parent_model = Parent.objects.get(id=parent)
    if set_model(parent_model, request):
        return redirect('parent', parent)
    return render(request, 'parent.html', {"parent": parent_model})


@login_required(login_url="/login/")
@employee_required()
def new_parent(request):
    parent = Parent()
    parent.save()
    redirect('/parent/' + str(parent.id) + "?edit=True")


@login_required(login_url="/login/")
@employee_required()
def new_student(request):
    student = Student()
    student.save()
    return redirect('/students/' + str(student.id) + "?edit=True")


@login_required(login_url="/login/")
@employee_required()
def archive_user(request, user):
    user = User.objects.get(id=user)
    user.is_archived = True
    user.save()
    return redirect('../')


@login_required(login_url="/login/")
def remove_user(request, user):
    user = Student.objects.get(id=user)
    user.delete()
    return redirect('/?operation=success')


@login_required(login_url="/login/")
def theme(request):
    request.user.theme = request.GET.get('theme')
    request.user.save()
    return HttpResponse("OK")


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


def logout(request):
    user_logout(request)
    return redirect('login')


def set_model(model, request):
    if len(request.GET) != 0:
        for name, value in request.GET.items():
            if name == 'fio':
                continue

            attr = None
            name = name.split('.')
            if len(name) > 1:
                attr = getattr(model, name.pop(0))
                for name_sp in name[:-1]:
                    attr = getattr(attr, name_sp)

                setattr(attr, name[-1], value)
                attr.save()
            else:
                setattr(model, name[-1], value)

        if request.GET.get('fio') is not None:
            last_name, first_name, patronymic = request.GET.get('fio').split(' ')
            setattr(model, 'last_name', last_name)
            setattr(model, 'first_name', first_name)
            setattr(model, 'patronymic', patronymic)
        model.save()
        return True
    else:
        return False
