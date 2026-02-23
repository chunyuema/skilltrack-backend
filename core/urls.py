from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    # The Login endpoint
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Application endpoints
    path("api/v1/profiles/", include("profiles.urls")),
    path("api/register/", RegisterView.as_view(), name="register"),
]
