from datetime import datetime

from django.db import models

from django.contrib.auth.models import User

class MessageThread(models.Model):
    """(MessageThread description)"""
    datetime_created = models.DateTimeField(blank=False, default=datetime.now)

    def __unicode__(self):
        return u"MessageThread"


class Message(models.Model):
    """(Message description)"""
    thread = models.ForeignKey(MessageThread)
    recipients = models.ManyToManyField(User)
    subject = models.CharField(blank=True, max_length=200)
    body = models.TextField(blank=True)
    datetime_sent = models.DateTimeField(blank=False, default=datetime.now)

    def __unicode__(self):
        return u"Message"
