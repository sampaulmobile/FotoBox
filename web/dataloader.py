#export DJANGO_SETTINGS_MODULE=jobious.settings
from django.core.management import setup_environ
import settings
import random as r

setup_environ(settings)
from django.contrib.auth.models import User
from reviews.models import Company, Division, DivisionReview
from profiles.models import UserProfile

companies = ["Microsoft", "Apple", "Facebook", "Google", "IBM", "Dropbox", '23andMe', 'Oracle', 'Vistaprint', 'Boeing']
divisions = ["Software Development", "UI Design", "Back-End Support", 'Mobile Platform', 'Project Manager', 'Site Traffic Analyst', 'Widget Guru']



classes = ["FR", "SO", "JR", "SR", "GR"]
posType = ["I", "P", "F"]
comments = ['I loved working here!', 'My boss was  hands-on, but let me define my project as I wanted', 'I would work here again.', 'I couldn\'t imagine working anywhere else. This is basically my dream position.', \
            'My project shipped and was used by 10,000 people in its first week. Where else ould you do that?', 'I got to open the API my project and now several thousand developers are actively developing with it. It is incredible toknow so many people use your stuff and that the company is so open to putting a young developer\'s stuff out there.',\
            'I had a pretty negative experience. My project was boring and my boss was always too busy too meet.', 'I had a lot of fun, but I am not sure if I would go back.']
first_names = ['Aaron', 'Barbara', 'Charles', 'Dale', 'Erica', 'Francine', 'Gertrude', 'Hector', 'Igor', 'John', 'Kate', 'Lester', 'Margaret', 'Nick', 'Ophelia', 'Pat', 'Quentin', 'Ricky', 'Slevin', 'Tad', 'Ulysses', 'Veronica', 'Whitney', 'Xenia', 'Yolanda', 'Zed']
last_names = ['Arthur', 'Becks', 'Clark', 'Dennis', 'Ernst', 'Fredericks', 'Greene', 'Harris', 'Jones', 'Kennedy', 'Long', 'Mason', 'North', 'Ortiz', 'Peters', 'Queenan', 'Ramos', 'Shaw', 'Tate', 'Underhill', 'Vetger', 'White']

for f in first_names:
    for l in last_names:

	uname = "%s.%s" % (f, l)
	u=User()
	u.username=uname
	u.first_name=f
	u.last_name = l
	u.email='%s@bogusemailaddress.com' % uname
	u.save()

users = User.objects.all()

for c in companies:
    company = Company(name = c)
    company.save()

comps = Company.objects.all()

for d in divisions:
    for c in comps:
        div = Division(name = d, company = c)
        div.save()

divs = Division.objects.all()

for u in users:
    for i in xrange(4):
	    d = divs[r.randint(0,len(divs)-1)]
	    position_type = posType[r.randint(0, 2)]
	    comment = comments[r.randint(0,len(comments)-1)]

	    dr = DivisionReview(reviewer=u, employer=d, position_type=position_type, year_taken=classes[i], overall=r.randint(1,5), pay=r.randint(1,5), hours=r.randint(1,5), difficulty=r.randint(1,5), comment=comment)
	    dr.save()