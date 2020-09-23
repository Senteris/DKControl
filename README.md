# DKControl
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Senteris/DKControl/Publish) ![GitHub](https://img.shields.io/github/license/Senteris/DKControl) ![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/Senteris/DKControl/django) ![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/Senteris/DKControl)  
Automation system for educational institutions
## How to install:  
- Install `Python 3.8` and `pipenv`
- Install requirements `pipenv install`
- Set  environment variables: `SECRET_KEY, HOST, DEBUG, DEPLOYMENT_TOKEN`
    - Linux: `export SECRET_KEY="key"`
    - Windows: `set SECRET_KEY="key"`
- Migrate database `python manage.py migrate`

# RU
Система автоматизации образовательных учреждений
## Как установить:  
- Установите `Python 3.8` и `pipenv`
- Установите зависимости `pipenv install`
- Настройте  переменные среды: `SECRET_KEY, HOST, DEBUG, DEPLOYMENT_TOKEN`
    - Linux: `export SECRET_KEY="key"`
    - Windows: `set SECRET_KEY="key"`
- Мигрируйте базу данных `python manage.py migrate`
