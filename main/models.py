from django.contrib.auth.models import AbstractUser
from django.db import models

#region Abstract
class BaseProfile(models.Model):
    patronymic = models.CharField('Отчество', max_length=16, blank=True, null=True)
    birthday = models.DateField('Дата рождения', null=True)

    GENDER_CHOISES = (
        ('Женский', 'Женский'),
        ('Мужской', 'Мужской')
    )
    gender = models.CharField('Пол', max_length=7, choices=GENDER_CHOISES, null=True)

    address = models.CharField('Адрес', max_length=128, null=True)
    phone = models.IntegerField('Телефон', null=True)

    class Meta:
        abstract = True

class Profile(BaseProfile):
    first_name = models.CharField("Имя", max_length=16)
    last_name = models.CharField("Фамилия", max_length=16)

    class Meta:
        abstract = True

#endregion

#region Models
class Union(models.Model):
    name = models.CharField("Название", max_length=64, null=True)


class Group(models.Model):
    name = models.CharField("Название", max_length=16)
    union = models.ForeignKey(Union, on_delete=models.CASCADE, verbose_name="Объединение", null=True)

class Timetable(models.Model):
    groups = models.ForeignKey(Group, on_delete=models.CASCADE)


class ElemOfTimetable(models.Model):
    begin_time = models.DateField("Время начала")
    end_time = models.DateField("Время конца")

    DAYS = (
        ('ПН', 'Понедельник'),
        ('ВТ', 'Вторник'),
        ('СР', 'Среда'),
        ('ЧТ', 'Четверг'),
        ('ПТ', 'Пятница'),
        ('СБ', 'Суббота'),
        ('ВС', 'Воскресенье'),
    )
    day = models.CharField('День', max_length=2, choices=DAYS)

    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)


class User(AbstractUser, BaseProfile):
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группы", null=True, blank=True)
    worktime = models.TimeField("Время работы", blank=True, null=True)

class Parent(Profile):

    def __str__(self):
        return f"Родитель: {self.first_name} {self.last_name} {self.patronymic:1}."

class Student(Profile):
    school = models.CharField('Школа', max_length=32)
    grade = models.CharField('Класс', max_length=3)
    groups = models.ManyToManyField(Group, related_name="Группы", blank=True)
    parents = models.ManyToManyField(Parent, related_name="Родители", blank=True)

    def __str__(self):
        return f"Ученик: {self.first_name} {self.last_name} {self.patronymic:1}. | Группа: {self.groups}"

#endregion