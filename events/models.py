from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


organizer = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='organized_events', null=True, blank=True)
    image = models.ImageField(
        upload_to='event_images/', default='event_images/default.jpg')

    def __str__(self):
        return self.name


class RSVP(models.Model):
    STATUS_CHOICES = [('GOING', 'Going'), ('NOT_GOING', 'Not Going')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='rsvps')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='GOING')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"
