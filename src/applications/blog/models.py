from datetime import datetime

from django.db import models


class Post(models.Model):
    title = models.TextField(unique=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    visible = models.BooleanField(default=False)

    def __str__(self):
        visible = "\N{FIRE}" if self.visible else "\N{SLEEPING SYMBOL}"
        msg = f'[{self.pk}] "{self.title}" {visible}'
        return msg

    class Meta:
        ordering = ["-created_at", "title", "pk"]
