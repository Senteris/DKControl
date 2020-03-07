from django.contrib.auth.models import AbstractUser
from django.db import models


class Group(models.Model):
    name = models.CharField("Название", max_length=16)

class Profile(models.Model):
    first_name = models.CharField("Имя", max_length=16)
    last_name = models.CharField("Фамилия", max_length=16)
    patronymic = models.CharField('Отчество', max_length=16, blank=True, null=True)
    birthday = models.DateField('Дата рождения')

    GENDER_CHOISES = (
        ('Женский', 'Женский'),
        ('Мужской', 'Мужской')
    )
    gender = models.CharField('Пол', max_length=7, choices=GENDER_CHOISES)

    address = models.CharField('Адрес', max_length=128)
    phone = models.IntegerField('Телефон')

    class Meta:
        abstract = True

class User(AbstractUser, Profile):
    #Ctrl+C Ctrl+V
    first_name = models.CharField("Имя", max_length=16)
    last_name = models.CharField("Фамилия", max_length=16)

    groups = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группы", null=True, blank=True)

#region models
class Parent(Profile):

    def __str__(self):
        return f"Родитель: {self.first_name} {self.last_name} {self.patronymic:1}."


class Student(Profile):
    school = models.CharField('Школа', max_length=32)
    grade = models.CharField('Класс', max_length=3)
    groups = models.ManyToManyField(Group, related_name="Группы", blank=True)
    parents = models.ManyToManyField(Parent, related_name="Родители", blank=True)

    def __str__(self):
        return f"Ученик: {self.first_name} {self.last_name} {self.patronymic:1}. | Группа: {self.groups} "
#endregion