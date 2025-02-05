from django.db import models
from Accounts.models import CustomUser

class UserActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.action} - {self.timestamp}.'
