from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User

from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.forms import ModelForm
from django import forms

from reviews.models import Division, DivisionReview

YEAR_CHOICES = tuple((str(n), str(n)) for n in reversed(range(1861, datetime.now().year + 4)))

DEGREE_CHOICES = (
    ('SB','Bachelor of Science'),
    ('SM','Master Degree'),
    ('MENG','Master of Engingeering'),
    ('PhD','Doctor of Philosophy'),
    ('ScD','Doctor of Science'),
    ('MBA','Master of Business Administration'),
)

COURSE_CHOICES = (
    ('1','Civil and Environmental Engineering'),
    ('2','Mechanical Engineering'),
    ('3','Materials Science'),
    ('4','Architecture'),
    ('5','Chemistry'),
    ('6','Electrical Engineering and Computer Science'),
    ('7','Biology'),
    ('8','Physics'),
    ('9','Brain and Cognitive Sciences'),
    ('10','Chemical Engineering'),
    ('11','Urban Studies and Planning'),
    ('12','Earth Atmospheric and Planetary Sciences'),
    ('14','Economics'),
    ('15','Management'),
    ('16','Aeronautics and Astronautics'),
    ('17','Political Science'),
    ('18','Mathematics'),
    ('20','Biological Engineering'),
    ('21','Humanities'),
    ('21A','Antropology'),
    ('21F','Foreign Languages and Literatures'),
    ('21H','History'),
    ('21L','Literature'),
    ('21M','Music'),
    ('21W','Writing and Humanistic Studies'),
    ('22','Nuclear Science and Engineering'),
    ('24','Linguistics and Philosophy'),
    ('ESD','Engineering Systems Division'),
    ('HST', 'Health Sciences & Technology'),
    ('MAS','Media Arts and Science'),
    ('STS','Science, Technology and Society'),
)

CLASS_CHOICES = (
    ('FR','Freshmen'),
    ('SO','Sophomore'),
    ('JR','Junior'),
    ('SR','Senior'),
    ('GR','Graduate')
)

    
class Degree(models.Model):
    """(Degree description)"""
    year = models.CharField(max_length=4, choices=YEAR_CHOICES)
    course = models.CharField(max_length=3, choices=COURSE_CHOICES)
    diploma_type = models.CharField(max_length=4, choices=DEGREE_CHOICES)
    
    def __unicode__(self):
        return ('%s %s %s' % (self.diploma_type, self.course, self.year))

class UserProfile(models.Model):
    user = models.OneToOneField(User)    

    #user_photo = models.ImageField(upload_to="/dir/path", height_field=150, width_field=100)
    dob = models.DateField(default=datetime.today() - timedelta(days=18*365.25))
    degrees = models.ManyToManyField(Degree)
    current_year = models.CharField(choices=CLASS_CHOICES, blank=True, max_length=100)
    favorites = models.ManyToManyField(DivisionReview)

    def __unicode__(self):
        return ('%s' % (self.user.username))

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

type_mapping = {'CharField':forms.CharField(max_length = 100), 'TextField': forms.CharField(widget = forms.Textarea),
	'BooleanField':forms.BooleanField(required = False), 'DateField':forms.DateField(widget = forms.DateInput),
	'URLField': forms.URLField(), 'EmailField': forms.EmailField()
	}

class EditUserModel(models.Model):
	"Model for editing user info form"
	
	first_name = models.CharField(max_length = 100)
	last_name = models.CharField(max_length = 100)
	dob = models.DateField()
	

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

signals.post_save.connect(create_user_profile, sender=User)
