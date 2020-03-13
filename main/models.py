from django.contrib.auth.models import AbstractUser
from django.db import models

#region Abstract
class BaseProfile(models.Model):
    patronymic = models.CharField('Отчество', max_length=16, null=True, blank=True)
    birthday = models.DateField('Дата рождения', null=True, blank=True)

    GENDER_CHOISES = (
        ('Женский', 'Женский'),
        ('Мужской', 'Мужской')
    )
    gender = models.CharField('Пол', max_length=7, choices=GENDER_CHOISES, null=True, blank=True)

    address = models.CharField('Адрес', max_length=128, null=True, blank=True)
    phone = models.IntegerField('Телефон', null=True, blank=True)

    class Meta:
        abstract = True

class Profile(BaseProfile):
    first_name = models.CharField("Имя", max_length=16)
    last_name = models.CharField("Фамилия", max_length=16)

    class Meta:
        abstract = True

#endregion

#region Models
class Zanyatie(models.Model): # Class Class xD
    date = models.DateField("Дата")
    elemOfTimetable = models.ForeignKey("ElemOfTimetable", verbose_name="Время", on_delete=models.SET_NULL)


class Union(models.Model):
    name = models.CharField("Название", max_length=64)

    def __str__(self):
        return  self.name


class Group(models.Model):
    name = models.CharField("Название", max_length=16)
    union = models.ForeignKey(Union, on_delete=models.CASCADE, verbose_name="Объединение", null=True)
    teacher = models.ForeignKey("User", verbose_name="Педагог", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return  f"{self.union.name}/{self.name}"


class Timetable(models.Model): # Расписание
    groups = models.ForeignKey(Group, on_delete=models.CASCADE)


class ElemOfTimetable(models.Model):
    begin_time = models.TimeField("Время начала")
    end_time = models.TimeField("Время конца")

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

    def __str__(self):
        return  self.timetable


class User(AbstractUser, BaseProfile):
    worktime = models.TimeField("Время работы", blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.patronymic}"

    class Meta:
        permissions = [
            ("has_groups", "Имеет группы"),
        ]


class Parent(Profile):

    def __str__(self):
        return f"Родитель: {self.first_name} {self.last_name} {self.patronymic:1}."


class Student(Profile):
    school = models.CharField('Школа', max_length=32, blank=True, null=True)
    grade = models.CharField('Класс', max_length=3, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="Группы", blank=True)
    parents = models.ManyToManyField(Parent, related_name="Родители", blank=True)

    def __str__(self):
        return f"Ученик: {self.first_name} {self.last_name} {self.patronymic:1}"

#endregion