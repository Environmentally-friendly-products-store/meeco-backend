from django.urls import include, path, re_path

from users.views import UserRegisterViewSet


app_name = 'api'


urlpatterns = [
    re_path(r'^jwt/', include('djoser.urls.jwt')),
    path('register/',
         UserRegisterViewSet.as_view({'post': 'create'}),
         name='register',
         ),
]
