from rest_framework.routers import DefaultRouter
from api.views import UserView, OverView

router = DefaultRouter()
router.register('', OverView, basename='')
router.register(r'users', UserView, basename='User')
