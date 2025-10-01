from django.urls import path

from custom_auth.views import CustomObtainAuthToken, LogoutView

urlpatterns = [
    path("token/", CustomObtainAuthToken.as_view(), name="token"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
