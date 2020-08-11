# DKControl
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Senteris/DKControl/Publish) ![GitHub](https://img.shields.io/github/license/Senteris/DKControl) ![Python](https://img.shields.io/badge/python-3.8-success)   
Automation system for educational institutions
## How to install:  
- Install `Python 3.8` and `pip`
- Install requirements `pip install -r requirements.txt`
- Set  environment variables: `SECRET_KEY, HOST, DEBUG, DEPLOYMENT_TOKEN`
    - Linux: `export SECRET_KEY="key"`
    - Windows: `set SECRET_KEY="key"`
- Migrate database `python manage.py migrate`

# RU
Система автоматизации образовательных учреждений
## Как установить:  
- Установите `Python 3.8` и `pip`
- Установите зависимости `pip install -r requirements.txt`
- Настройте  переменные среды: `SECRET_KEY, HOST, DEBUG, DEPLOYMENT_TOKEN`
    - Linux: `export SECRET_KEY="key"`
    - Windows: `set SECRET_KEY="key"`
- Мигрируйте базу данных `python manage.py migrate`
