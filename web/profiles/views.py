from django.template import RequestContext, loader
from django.http import HttpResponse
from reviews.models import Division, DivisionReview
from profiles.forms import *
from django.forms.models import modelformset_factory
from profiles.models import UserProfileForm
from profiles.models import UserProfile, User
from django.shortcuts import render_to_response
from django.contrib.csrf.middleware import csrf_exempt
from django.shortcuts import redirect

def index(request):
    t = loader.get_template('index.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))
	
def review_list(request):
	t = loader.get_template('index.html')
	division_list = Division.objects.all()[:7]
	division_reviews = DivisionReview.objects.all()[:200]
	c = RequestContext(request, {'division_list':division_list, 'division_reviews':division_reviews})
	return HttpResponse(t.render(c))
	
def account_info(request):
    t = loader.get_template('account_info.html')
    user = request.user
    f = UserProfileForm()
    
    return render_to_response("account_info.html", {"form": f},context_instance=RequestContext(request))

def toggle_favorite(request):
    prof = request.user.get_profile()
    favs = prof.favorites.all()
    dr = DivisionReview.objects.get(id=request.POST.get('stardr'))

    if dr in favs:
        prof.favorites.remove(dr)
    else:
        prof.favorites.add(dr)
        
    prof.save()
    url = request.META['HTTP_REFERER']
    return HttpResponseRedirect(url)

toggle_favorite = csrf_exempt(toggle_favorite)

def account_update(request):
	t = loader.get_template('account_info.html')
	first_name = request.POST.get('first_name', '')
	last_name = request.POST.get('last_name', '')
	user = request.user
	user.first_name = first_name
	user.last_name = last_name
	user.save()
	c = RequestContext(request)
	return HttpResponse(t.render(c))	