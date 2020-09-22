from django.db import models
from django.contrib.auth.models import User


class Events(models.Model):
    title = models.CharField(max_length=150)
    description = description = models.TextField()
    location = models.CharField(max_length=150)
    datetime = models.DateField()
    seats = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Book(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)

    def __str__(self):
        self.event.seats-=1
        return self.event.title
