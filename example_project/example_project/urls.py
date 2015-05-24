from django.conf.urls import include, url

from example_project import views


urlpatterns = [

    url(r'^test$', views.test),
]
