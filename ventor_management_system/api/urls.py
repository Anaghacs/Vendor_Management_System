from django.urls import path
from vendors.views import index, vendors

urlpatterns = [
    path("index/", index, name = "index"),
    path("vendors/", vendors, name = "vendors"),
]