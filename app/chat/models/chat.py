from django.db import models


class Chat(models.Model):
    user_prompt = models.CharField(max_length=100)
