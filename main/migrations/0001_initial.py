# Generated by Django 3.0.4 on 2020-03-07 13:15

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=16, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=16, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=16, null=True, verbose_name='Отчество')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('gender', models.CharField(choices=[('Женский', 'Женский'), ('Мужской', 'Мужской')], max_length=7, verbose_name='Пол')),
                ('address', models.CharField(max_length=128, verbose_name='Адрес')),
                ('phone', models.IntegerField(verbose_name='Телефон')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=16, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=16, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=16, null=True, verbose_name='Отчество')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('gender', models.CharField(choices=[('Женский', 'Женский'), ('Мужской', 'Мужской')], max_length=7, verbose_name='Пол')),
                ('address', models.CharField(max_length=128, verbose_name='Адрес')),
                ('phone', models.IntegerField(verbose_name='Телефон')),
                ('school', models.CharField(max_length=32, verbose_name='Школа')),
                ('grade', models.CharField(max_length=3, verbose_name='Класс')),
                ('groups', models.ManyToManyField(blank=True, related_name='Группы', to='main.Group')),
                ('parents', models.ManyToManyField(blank=True, related_name='Родители', to='main.Parent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('patronymic', models.CharField(blank=True, max_length=16, null=True, verbose_name='Отчество')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('gender', models.CharField(choices=[('Женский', 'Женский'), ('Мужской', 'Мужской')], max_length=7, verbose_name='Пол')),
                ('address', models.CharField(max_length=128, verbose_name='Адрес')),
                ('phone', models.IntegerField(verbose_name='Телефон')),
                ('first_name', models.CharField(max_length=16, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=16, verbose_name='Фамилия')),
                ('groups', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Group', verbose_name='Группы')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
