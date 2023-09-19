from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from orders.views import OrderViewSet
from products.views import ProductViewSet
from users.views import UserRegisterViewSet, me

app_name = "api"

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"products", OrderViewSet)


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
    path("", include(router.urls)),
]
