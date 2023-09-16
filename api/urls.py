from django.urls import path
from rest_framework_simplejwt import views

from users.views import UserRegisterViewSet, me

app_name = "api"


urlpatterns = [
    path(
        "register/",
        UserRegisterViewSet.as_view({"post": "create"}),
        name="register",
    ),
    path("token/", views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", views.TokenVerifyView.as_view(), name="token_verify"),
    path("users/me/", me, name="user_me"),
]
