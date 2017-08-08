from django.conf.urls import url, include
from .views import WeChat

urlpatterns = [
  url(r'^$', WeChat.as_view()),
]
