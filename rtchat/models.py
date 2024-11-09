from django.db import models
from django.contrib.auth.models import User

class GroupMessage(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.text:
            return f'{self.author.username} : {self.text}'
    
    class Meta:
        ordering = ['-created']

