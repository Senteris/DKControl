from django.contrib.auth.models import AbstractUser
from django.db import models

class Group(models.Model):
    name = models.CharField("Название", max_length=16)
    educator = models.ManyToManyField("Educator", "Преподаватель")

#region Abstract
class AParent():



class AStudent():
    school = models.CharField('Школа', max_length=32)
    grade = models.CharField('Класс', max_length=3)
    groups = models.ManyToManyField(Group, related_name="группы", null=True, blank=True)
    parents = models.ManyToManyField("Parent", related_name="группы", null=True, blank=True)

class AEducator():

#endregion

#region abstract classes
class Person():
    firstName = models.CharField("Имя", max_length=16)
    lastName = models.CharField("Фамилия", max_length=16)
    patronymic = models.CharField('Отчество', max_length=16, blank=True, null=True)
    birthday = models.DateField('Дата рождения')

    GENDER_CHOISES = (
        'Женский', 'Женский',
        'Мужской', 'Мужской'
    )
    gender = models.CharField('Пол', max_length=7, choices=GENDER_CHOISES)

    address = models.CharField('Адрес', max_length=128)
    phone = models.IntegerField('Телефон', max_length=11)

class User(AbstractUser, Person):
#endregion

#region models
class Parent(AParent, User):

    def __str__(self):
        return f"Родитель: {self.first_name} {self.last_name} {self.patronymic:1}."


class Student(AStudent, User):

    def __str__(self):
        return f"Ученик: {self.first_name} {self.last_name} {self.patronymic:1}. | Группа: {self.group} "

#endregion