from django.template import RequestContext, loader
from django.http import HttpResponse
from reviews.models import Division, DivisionReview

def index(request):
    t = loader.get_template('index.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))