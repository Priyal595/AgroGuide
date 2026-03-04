from django.db import models
from django.contrib.auth.models import User


class VoiceQuery(models.Model):
    QUERY_TYPE_CHOICES = [
        ('text', 'Text'),
        ('audio', 'Audio'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='voice_queries'
    )
    query = models.TextField()
    response = models.TextField()
    query_type = models.CharField(
        max_length=10,
        choices=QUERY_TYPE_CHOICES,
        default='text'
    )
    language = models.CharField(max_length=10, default='en')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} | {self.query_type} | {self.query[:40]}"
