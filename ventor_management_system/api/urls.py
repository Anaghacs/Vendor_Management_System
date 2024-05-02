from django.urls import path
from vendors.views import index

urlpatterns = [
    path("index/", index, name = "index"),
]