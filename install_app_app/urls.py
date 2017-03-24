from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^page/', views.page),
    url(r'^tile/', views.page)
]