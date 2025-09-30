from django.urls import path

from contacts.views import ContactQrView

urlpatterns = [
    path("send-qr/", ContactQrView.as_view(), name="send-qr"),
]
