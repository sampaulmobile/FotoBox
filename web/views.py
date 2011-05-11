from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext, loader
from django.http import HttpResponse

#import models
from web.reviews.models import DivisionReview

def index(request):
    some_reviews = DivisionReview.objects.all().order_by('id')[:10]
    t = loader.get_template('index.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))