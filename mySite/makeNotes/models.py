from django.db import models
from django.utils import timezone

class Note(models.Model):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else self.created_at.strftime('%Y-%m-%d %H:%M:%S')