from django.db import models
from django.contrib.auth.models import User


class TopSecret(models.Model):

    title = models.CharField(" 📌 Title ", max_length=100)
    username = models.CharField(" 🧔 Username", max_length=100, blank=True)
    password = models.CharField("🔑 Password", max_length=100, default="")
    message = models.CharField(
        "💬 Small Message?", max_length=100, blank=True, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
