from django.contrib.auth.models import AbstractUser
from django.db import models


#region Interfaces
class IParent():

class IStudent():

#endregion

#region abstract classes
class User(AbstractUser):
    patronymic = models.CharField('Отчество', max_length=32, blank=True, null=True)
    birthday = models.DateField('Дата рождения')

    GENDER_CHOISES = (
        'Женский', 'Женский',
        'Мужской', 'Мужской'
    )
    gender = models.CharField('Пол', max_length=7, choices=GENDER_CHOISES)


#endregion

#region models
class Parent(IParent, User):


class Student(IStudent, User):

#endregion