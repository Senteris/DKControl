from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.renderers import JSONOpenAPIRenderer

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from api.views import UserView, OverviewView

router = DefaultRouter()
router.register(r'users', UserView, basename='User')
router.APIRootView = OverviewView

urlpatterns = [
    path('', include(router.urls)),
    path('openapi/', get_schema_view(
        title="DKControl",
        description="API",
        version="1.0.0",
        renderer_classes=[JSONOpenAPIRenderer]
    ), name='openapi-schema'),
    path('redoc/', TemplateView.as_view(
        template_name='api/redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),
    path('auth/', include('rest_framework.urls')),
]
