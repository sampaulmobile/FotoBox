from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from reviews.models import Division, DivisionReview
from profiles.forms import *
from django.forms.models import modelformset_factory
from profiles.models import UserProfileForm
from profiles.models import UserProfile, User
from django.shortcuts import render_to_response,redirect
from django.contrib.csrf.middleware import csrf_exempt
from django.shortcuts import redirect

import flickrapi
def getURL(picSizes):
    #gets the best size for a photo and returns its URL
    d = {}
    for size in picSizes:
		url = size.attrib['source']
		temp = url[-6:-4]
		if "_" in temp:
			return url[0:-6]+".jpg"
		else:
			return url
		
		
def getPhotosByUID(f, id):
    return f.photos_search(user_id=id)[0]

def getPhotoURL(f, p):
    picSizes = f.photos_getSizes(photo_id=p.attrib['id'])[0]
    return getURL(picSizes) 

def listUserPhotoURLs(f, uid):
    l = []
    photos = getPhotosByUID(f, uid)
    for photo in photos:
        l.append(getPhotoURL(f, photo))
    return l

def listUserPhotoTitles(f, uid):
    l = []
    photos = getPhotosByUID(f, uid)
    for photo in photos:
        l.append(photo.attrib['title'])
    return l

def getUID(f, uname):
    person = f.people_findByUsername(username=uname)[0]
    return person.attrib['nsid']

def getPhotosForUser(f, uname):
    uid = getUID(f, uname)
    l = []
    photos = getPhotosByUID(f, uid)
    for photo in photos:
        temp = {}
        temp['url'] = getPhotoURL(f, photo)
        temp['title'] = photo.attrib['title']
        l.append(temp)
    return l
	
def getPanoPhotos(f, uid):
    l = []
    photos = f.photos_search(user_id=uid)[0]
    for photo in photos:
        pid = photo.attrib['id']
        if len(f.photos_getInfo(photo_id=pid)[0][9]) != 0:
            temp = {}
            temp['id'] = pid
            temp['url'] = getPhotoURL(f, photo)
            temp['title'] = photo.attrib['title']
            l.append(temp)
    return l

def getPoints(f, pid1, pid2):     
    l = []
    img1x = ""
    img1y = ""
    img2x = ""
    img2y = ""
    
    notes1 = f.photos_getInfo(photo_id=pid1)[0][9]
    for note1 in notes1:
        img1x += note1.attrib['x'] + '-'
        img1y += note1.attrib['y'] + '-'
    l.append(img1x[0:-1])
    l.append(img1y[0:-1])
    notes2 = f.photos_getInfo(photo_id=pid2)[0][9]
    for note2 in notes2:
        img2x += note2.attrib['x'] + '-'
        img2y += note2.attrib['y'] + '-'
    l.append(img2x[0:-1])
    l.append(img2y[0:-1])
    return l

	
def getURLFromPID(f, pid):
	photo = f.photos_getInfo(photo_id=pid)[0]
	return getPhotoURL(f, photo)

def convertURL(s):
	s = s.replace(":", "%3A")
	s = s.replace("/", "%2F")
	return s
	
def index(request):
    t = loader.get_template('index.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))

def fotobox(request):
    t = loader.get_template('fotobox.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))

def flickr_login(request):
    t = loader.get_template('foto_login.html')
    c = RequestContext(request)
    return HttpResponse(t.render(c))
	
def flickr_login_callback(request):
	api_key = 'e978df8e79c65322505760ff3045d67b'
	flickr = flickrapi.FlickrAPI(api_key, cache=True)
	username = request.GET.get("username")
	photos = getPhotosForUser(flickr, username)
	t = loader.get_template('foto_list.html')
	length = len(photos)
	y_range = xrange(length/4)
	x_range = xrange(4)
	c = RequestContext(request,{'photos':photos, 'username':username, 'y_range':y_range, 'x_range':x_range})
	return HttpResponse(t.render(c))

def editFoto(request):
	url = request.GET.get("url")
	type = request.GET.get("edit_type")
	username = request.GET.get("username")
	if type=="seam":
		t = loader.get_template('fotobox_seam.html')
	elif type=="spanish":
		t = loader.get_template('fotobox_spanish.html')
	elif type=="linear_demosaic":
		t = loader.get_template('linear_demosaic.html')
	elif type=="median_demosaic":
		t = loader.get_template('median_demosaic.html')
	elif type=="tonemap_gaussian":
		t = loader.get_template('tonemap_gaussian.html')
	elif type=="tonemap_bilateral":
		t = loader.get_template('tonemap_bilateral.html')
	c = RequestContext(request, {'url':url, 'username':username})
	return HttpResponse(t.render(c))
	
def panorama_manual(request):
	api_key = 'e978df8e79c65322505760ff3045d67b'
	flickr = flickrapi.FlickrAPI(api_key, cache=True)
	username = request.GET.get("uname")
	uid = getUID(flickr, username)
	photos = getPanoPhotos(flickr, uid)
	c = RequestContext(request,{'photos':photos, 'username':username})
	t = loader.get_template('panorama_list.html')
	return HttpResponse(t.render(c))
	
def panorama_callback(request):
	api_key = 'e978df8e79c65322505760ff3045d67b'
	flickr = flickrapi.FlickrAPI(api_key, cache=True)
	ids = request.GET.getlist(u'id')
	url1 = getURLFromPID(flickr, ids[0])
	url2 = getURLFromPID(flickr, ids[1])
	username = request.GET.get("username")
	points = getPoints(flickr, ids[0], ids[1])
	parameters = "username="+username
	parameters += "&url1="+convertURL(url1)
	parameters+= "&url2="+convertURL(url2)
	parameters += "&pts1x="+points[0]
	parameters += "&pts1y="+points[1]
	parameters += "&pts2x="+points[2]
	parameters += "&pts2y="+points[3]
	url = "http://127.0.0.1:7000/cgi-bin/manual_panorama.exe?"+parameters
	return HttpResponseRedirect(url)

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
