from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from events.views import EventViewSet
from orders.views import OrderViewSet
from products.views import CategoryViewSet, ProductViewSet
from users.views import ShoppingCartViewSet, UserRegisterViewSet, me

app_name = "api"

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"events", EventViewSet)

urlpatterns = [
    path(
        "register/",
        UserRegisterViewSet.as_view({"post": "create"}),
        name="register",
    ),
    path(
        "token/",
        views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "token/verify/",
        views.TokenVerifyView.as_view(),
        name="token_verify",
    ),
    path("users/me/", me, name="user_me"),
    # path(
    #     'products/<int:product_id>/favorite/',
    #     FavoriteView.as_view(),
    # ),
    path(
        "products/<int:product_id>/shopping_cart/",
        ShoppingCartViewSet.as_view(),
    ),
    path("", include(router.urls)),
]
