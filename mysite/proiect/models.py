from django.db import models
from django.utils import timezone
from datetime import datetime

class Messages(models.Model):
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    dateSent = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.sender

    def __str__(self):
        return self.receiver
    


