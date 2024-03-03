from rest_framework import serializers
from chat.models.chat_model import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['user_prompt']
