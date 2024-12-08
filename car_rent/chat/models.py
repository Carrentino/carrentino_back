from django.db import models

from users.models import User


class Chat(models.Model):
    participants = models.ManyToManyField(
        User, related_name='chats', verbose_name='Участники чата'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Chat for Order {self.order.id}"

class Message(models.Model):
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE,
        related_name='messages', verbose_name='Чат'
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='messages', verbose_name='Отправитель'
    )
    content = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')

    def __str__(self):
        return f"Message from {self.sender} in Chat {self.chat.id}"
