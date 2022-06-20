from unixtimestampfield.fields import UnixTimeStampField

from django.db import models

from authapi.models import CustomUser


class ToDo(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    due = UnixTimeStampField(use_numeric=True, default=0.0)
    completed = models.BooleanField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
