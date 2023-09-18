from django.urls import path, include
from rest_framework_simplejwt import views
from rest_framework.routers import DefaultRouter

from users.views import UserRegisterViewSet, me
from products.views import ProductViewSet

app_name = "api"

router = DefaultRouter()
router.register(r'products', ProductViewSet)


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
    path("", include(router.urls))
]
