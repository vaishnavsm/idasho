from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^dash/', views.dash),
    url(r'^request/',views.req),
    url(r'^install/',views.install_app),
    url(r'', views.login)
]