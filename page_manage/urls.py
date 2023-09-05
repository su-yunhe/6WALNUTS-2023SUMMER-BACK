from django.urls import path
from .views import *


urlpatterns = [
      path("page_add", page_add),
      path("page_get", page_get),
      path("change_page_vaild", change_page_vaild),
    ]
