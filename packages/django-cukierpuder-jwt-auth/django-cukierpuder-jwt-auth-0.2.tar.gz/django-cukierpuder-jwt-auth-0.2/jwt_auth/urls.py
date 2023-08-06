from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserCreate,
    UserList,
    UserDetail
)


urlpatterns = [
    path('token/obtain/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', UserCreate.as_view()),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>', UserDetail.as_view(), name='user-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
