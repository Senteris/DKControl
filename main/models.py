import datetime as dt
from django.contrib.auth.models import AbstractUser
from django.db import models

#region Abstract
class BaseProfile(models.Model):
    patronymic = models.CharField('Отчество', max_length=16, null=True, blank=True)
    birthday = models.DateField('Дата рождения', null=True, blank=True)

    GENDER_CHOICES = (
        ('Женский', 'Женский'),
        ('Мужской', 'Мужской'),
    )
    gender = models.CharField('Пол', max_length=7, choices=GENDER_CHOICES, null=True, blank=True)

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
class Note(models.Model):
    student = models.ForeignKey("Student", verbose_name="Студент", on_delete=models.CASCADE)
    user = models.ForeignKey("User", verbose_name="Пользователь", on_delete=models.CASCADE)
    text = models.TextField("Текст")


class StudySession(models.Model): # Class Class x
    date = models.DateTimeField("Дата и время начала")
    group = models.ForeignKey("Group", verbose_name="Группа", on_delete=models.CASCADE)
    cancelReason = models.CharField("Причина отмены", max_length=128, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.group.name} [{self.date.strftime('%Y.%m.%d %H:%M:%S')}]"

class Attending(models.Model):
    student = models.ForeignKey("Student", verbose_name="Студент", on_delete=models.CASCADE)
    isAttend = models.BooleanField("Посетил", default=False)
    studySession = models.ForeignKey(StudySession, verbose_name="Занятие", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.last_name} -> {self.studySession.__str__()}"

class Union(models.Model):
    name = models.CharField("Название", max_length=64, default="No name")
    occupationReason = models.CharField("Причина занятости", max_length=128, null=True, blank=False, default=None)

    logo = models.ForeignKey("Logo", verbose_name="Лого", blank=True, null=True, on_delete=models.SET_NULL) # TODO Под вопросом
    def __str__(self):
        return  self.name


class Group(models.Model):
    name = models.CharField("Название", max_length=16)
    union = models.ForeignKey(Union, on_delete=models.CASCADE, verbose_name="Объединение", null=True)
    teacher = models.ForeignKey("User", verbose_name="Педагог", on_delete=models.SET_NULL, null=True, blank=True)
    # TODO нужно ли архивировать группы?

    def __str__(self):
        return f"{self.union.name}/{self.name}"


class TimetableElem(models.Model):
    beginTime = models.TimeField("Время начала")
    endTime = models.TimeField("Время конца", blank=True, default="00:00:00")

    DAYS = (
        ('ПН', 'Понедельник'),
        ('ВТ', 'Вторник'),
        ('СР', 'Среда'),
        ('ЧТ', 'Четверг'),
        ('ПТ', 'Пятница'),
        ('СБ', 'Суббота'),
    )
    day = models.CharField('День', max_length=2, choices=DAYS)
    group = models.ForeignKey("Group", verbose_name="Группа", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.endTime = (dt.datetime.combine(dt.date(1, 1, 1), self.beginTime) + dt.timedelta(
            minutes=100)).time()  # С костыля, ША! FullStackOverflow наше всё (работает на божей силе:b)
        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.day} в {self.beginTime.strftime('%H:%M')}-{self.endTime.strftime('%H:%M')}"


class User(AbstractUser, BaseProfile):
    union = models.ForeignKey(Union, verbose_name="Объединение", on_delete=models.SET_NULL, blank=True, null=True)
    profileIcon = models.ImageField("Фото профиля", upload_to="profileIcon", blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.patronymic}"

    class Meta:
        permissions = [
            ("has_groups", "Имеет группы"),
            ("edit_any_studySession", "Редактирует любые занятия"),
            ("cancel_studySession", "Отменяет занятия"),
        ]


class Parent(Profile):

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.patronymic:1}"


class Student(Profile):
    school = models.CharField('Школа', max_length=32, blank=True, null=True)
    grade = models.CharField('Класс', max_length=3, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="students", verbose_name="Ученики", blank=True)
    parents = models.ManyToManyField(Parent, related_name="childs", verbose_name="Родители", blank=True)

    isDeleted = models.BooleanField('Удалён', default=False, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.patronymic:1}"
#endregion

#region Other models
class Logo(models.Model):
    name = models.CharField("Название", max_length=16)
    link = models.ImageField("Иконка", upload_to="logo")

    def __str__(self):
        return self.name
#endregion