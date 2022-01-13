"""
app URLS
"""
from django.contrib import admin
from django.urls import path
from app.views import (
    home,
    login,
    signup,
    add_TopSecret,
    signout,
    delete_TopSecret,
    encoded_password,
    details_view,
)

# App url pattern
urlpatterns = [
    path("", home, name="home"),
    path("login", login, name="login"),
    path("signup", signup),
    path("add-TopSecret/", add_TopSecret),
    path("delete-TopSecret/<int:id>", delete_TopSecret),
    path("logout/", signout),
    path("encoded_password/", encoded_password),
    path("details", details_view, name="details"),
]
