from django.db import models
import datetime

from django.contrib.auth.models import User
from web.reviews.models import Division, DivisionReview

class DivisionFavorite(models.Model):
    """(Favoirte description)"""
    user = models.ForeignKey(User)
    division = models.ForeignKey(Division)
    time_favorited = models.DateTimeField(blank=True, default=datetime.datetime.now)

    def __unicode__(self):
        return "%s:%s" % (self.user, self.review)

class ReviewFavorite(models.Model):
    """(Favoirte description)"""
    user = models.ForeignKey(User)
    review = models.ForeignKey(DivisionReview)
    time_favorited = models.DateTimeField(blank=True, default=datetime.datetime.now)

    def __unicode__(self):
        return "%s:%s" % (self.user, self.review)