import datetime
from django.db import models

from django.contrib.auth.models import User

class Company(models.Model):
    """(Company description)"""
    name = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return "%s" % self.name
    
      
class Division(models.Model):
    """(Division description)"""
    name = models.CharField(blank=True, max_length=100)
    company = models.ForeignKey(Company)
    
    def __unicode__(self):
        return "%s %s" % (self.company, self.name)
    

POSITION_TYPE_CHOICES = (
    ('I', 'Internship'),
    ('P', 'Part-time'),
    ('F', 'Full-time')
)
CLASS_CHOICES = (
    ('FR','Freshman'),
    ('SO','Sophomore'),
    ('JR','Junior'),
    ('SR','Senior'),
    ('GR','Graduate')
)

RANKING_CHOICES = zip( range(1,6), range(1,6) )
class DivisionReview(models.Model):
    """(PositionReview description)"""
    #date_posted = models.DateTimeField(blank=True, default=datetime.datetime.now)
    
    reviewer = models.ForeignKey(User)
    employer = models.ForeignKey(Division)
    position_title = models.CharField(blank=True, max_length=100)
    position_type = models.CharField(choices=POSITION_TYPE_CHOICES, blank=True, max_length=1)

    views = models.IntegerField(default=0)

    year_taken = models.CharField(choices=CLASS_CHOICES,blank=True, max_length=2)
    
    overall = models.IntegerField(choices=RANKING_CHOICES, blank=True, null=True)
    pay = models.IntegerField(choices=RANKING_CHOICES, blank=True, null=True)
    hours = models.IntegerField(choices=RANKING_CHOICES, blank=True, null=True)
    difficulty = models.IntegerField(choices=RANKING_CHOICES, blank=True, null=True)
    
    comment = models.TextField(blank=True)

    def __unicode__(self):
        return "%s:%s" % (self.employer, self.reviewer)

