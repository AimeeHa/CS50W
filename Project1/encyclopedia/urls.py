from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<slug:title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("newpage", views.create, name="newpage"),
    path("edit/<slug:title>", views.edit, name="edit"),
    path("random", views.rand, name="random"),
]
