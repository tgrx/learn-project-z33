from datetime import datetime

from django.db import models
from django.urls import reverse_lazy


class Post(models.Model):
    title = models.TextField(unique=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    visible = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse_lazy("blog:post", kwargs={"pk": self.pk})

    def __str__(self):
        visible = "\N{FIRE}" if self.visible else "\N{SLEEPING SYMBOL}"
        msg = f'[{self.pk}] "{self.title}" {visible}'
        return msg

    class Meta:
        ordering = ["-created_at", "title", "pk"]
