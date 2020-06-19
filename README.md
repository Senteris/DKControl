# DKControl
Educational automation system
## How to install:  
- Install `Puthon 3.8`
- Install requirements `pip install -r requirements.txt`
- Set  environment variables: `SECRET_KEY, HOST, DEBUG, DEPLOYMENT_TOKEN`
    - Linux: `export SECRET_KEY="key"`
    - Windows: `set SECRET_KEY="key"`
- Migrate database `python manage.py migrate`
