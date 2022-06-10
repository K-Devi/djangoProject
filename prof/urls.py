from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers, permissions
from . import views
# from .views import Login

router = routers.DefaultRouter()
router.register(r'subjects', views.SubjectViewSet)
router.register(r'chapters', views.ChaptersViewSet)
router.register(r'themes', views.QuestionThemeViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'catalogs', views.CatalogViewSet)
router.register(r'images', views.ImageViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'topic-rules', views.TopicRuleViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Test Manager API",
      default_version='v1',
      description="Test API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('login/', Login.as_view(), name='login'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('pdf/', views.topic_generator, name='pdf')
]