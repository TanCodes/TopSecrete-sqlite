from django.forms import ModelForm

from app.models import TopSecret


class TopSecretForm(ModelForm):
    class Meta:
        model = TopSecret
        fields = ["title", "username", "password", "message"]
