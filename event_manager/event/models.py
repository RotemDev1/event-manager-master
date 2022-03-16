from django.db import models


from django.contrib.auth import get_user_model
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now=False, null=True)
    end_date = models.DateTimeField(auto_now=False, null=True)
    capacity = models.IntegerField(default=0)
    place = models.CharField(max_length=120, default="-")
    cancelled = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class CancelledEvent(models.Model):
    EventId = models.IntegerField(default=0)

    def __str__(self):
        return str(self.EventId)


class EventUpdates(models.Model):
    EventId = models.IntegerField(default=0)
    announcement = models.TextField()
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.EventId) + ' - ' + str(self.announcement)


class RateEvent(models.Model):
    EventId = models.IntegerField(default=0)
    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(rate__range=(1, 5)), name='valid_rate'),
            UniqueConstraint(fields=['user', 'EventId'], name='rating_once')
        ]

    def __str__(self):
        return str(self.EventId) + ' - ' + str(self.user) + ' - ' + str(self.rate)


class EventComment(models.Model):
    EventId = models.IntegerField(default=0)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        return str(self.text) + ' by ' + str(self.user)


class EventRecommend(models.Model):
    EventId = models.IntegerField(default=0)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        return str(self.text) + ' by ' + str(self.user)


class MyEvent(models.Model):
    EventId = models.IntegerField(default=0)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'EventId'], name='events_once')
        ]

    def __str__(self):
        return str(self.EventId) + ' - ' + str(self.user)


class ReportComment(models.Model):
    EventId = models.IntegerField(default=0)
    CommentId = models.ForeignKey(EventComment, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'EventId', 'CommentId'], name='report_once')
        ]

    def __str__(self):
        return str(self.EventId) + ' - ' + str(self.user)


class ChooseComment(models.Model):
    EventId = models.IntegerField(default=0)
    CommentId = models.ForeignKey(EventComment, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'EventId', 'CommentId'], name='choose_once')
        ]

    def __str__(self):
        return str(self.EventId) + ' - ' + str(self.CommentId) + ' - ' + str(self.user)
