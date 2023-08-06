import datetime

from django.db import models
from django.utils import timezone


class Input(models.Model):
    input_text = models.CharField(max_length=250)

    def __str__(self):
        return self.input_text


class Question(models.Model):
    # ...
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
