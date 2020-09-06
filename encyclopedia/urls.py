from django.urls import path

from . import views

#app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("<str:name>", views.greet, name="greet"),
    path("<str:title>/edit", views.edit, name="edit"),
    path("<str:title>/delete", views.delete, name="delete")
]
