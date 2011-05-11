from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.db.models import Avg, Count, Max, Min, StdDev, Sum
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from reviews.models import Division, DivisionReview, Company
import re

from django.db.models import Q

def get_annotated_divisions():
    div_results = DivisionReview.objects.all()
    
    div_results = div_results.annotate(num_reviews=Count('id'))
    div_results = div_results.annotate(avg_rating = Avg('overall'))
    div_results = div_results.annotate(avg_pay = Avg('pay'))
    div_results = div_results.annotate(avg_hours = Avg('hours'))
    div_results = div_results.annotate(avg_difficulty = Avg('difficulty'))
    
    div_results = div_results.order_by('-avg_rating')
    return div_results

def index(request):
    #construct template variables
    context = {}
    
    division_list = get_annotated_divisions()
    
    paginator = Paginator(division_list, 25)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        page_divisions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_divisions = paginator.page(paginator.num_pages)
    
    context['divisions'] = page_divisions
    
    #cpnstruct context and template
    c = RequestContext(request, context)
    t = loader.get_template('reviews/division_list.html')
    
    return HttpResponse(t.render(c))

def review(request, review_id):
	t = loader.get_template('review.html')
	review = DivisionReview.objects.get(id=review_id)
	difficulty = xrange(review.difficulty)
	hours = xrange(review.difficulty)
	pay = xrange(review.pay)
	overall = xrange(review.overall)
	c = RequestContext(request, {'review':review, 'difficulty':difficulty, 'hours':hours, 'pay':pay, 'overall':overall})
	return HttpResponse(t.render(c))
	
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
        
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
	
def search_reviews(request):
    dr_list = DivisionReview.objects.all()
    string = request.POST.get('searchbar')
    if string is None:
        return redirect(request.META['HTTP_REFERER'])
    fields = ['employer__company__name','employer__name','reviewer__username','comment']
    query = get_query(string, fields)
    if query == None:
        return redirect(request.META['HTTP_REFERER'])
    div_results = DivisionReview.objects.filter(query)
    
    div_results = div_results.annotate(num_reviews=Count('id'))
    div_results = div_results.annotate(avg_rating = Avg('overall'))
    div_results = div_results.annotate(avg_pay = Avg('pay'))
    div_results = div_results.annotate(avg_hours = Avg('hours'))
    div_results = div_results.annotate(avg_difficulty = Avg('difficulty'))
    
    div_results = div_results.order_by('-avg_rating')
    
    paginator = Paginator(div_results, 25)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        page_divisions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_divisions = paginator.page(paginator.num_pages)
    context = {}
    context['divisions'] = page_divisions
    
    #cpnstruct context and template
    c = RequestContext(request, context)
    t = loader.get_template('reviews/search_list.html')
    
    return HttpResponse(t.render(c))
	
def create_review(request):
    c = RequestContext(request)
    t = loader.get_template('create_review.html')
    return HttpResponse(t.render(c))
    
def my_reviews(request):
    fields = ['reviewer__username']
    query = get_query(request.user.username, fields)
    
    div_results = DivisionReview.objects.filter(query)
    
    div_results = div_results.annotate(num_reviews=Count('id'))
    div_results = div_results.annotate(avg_rating = Avg('overall'))
    div_results = div_results.annotate(avg_pay = Avg('pay'))
    div_results = div_results.annotate(avg_hours = Avg('hours'))
    div_results = div_results.annotate(avg_difficulty = Avg('difficulty'))
    
    div_results = div_results.order_by('-avg_rating')
    paginator = Paginator(div_results, 25)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        page_divisions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_divisions = paginator.page(paginator.num_pages)
        
    context = {}
    context['divisions'] = page_divisions
    
    #cpnstruct context and template
    c = RequestContext(request, context)
    t = loader.get_template('reviews/search_list.html')
    
    return HttpResponse(t.render(c))
    
def list_favorites(request):
    div_results = request.user.get_profile().favorites.all()
    
    div_results = div_results.annotate(num_reviews=Count('id'))
    div_results = div_results.annotate(avg_rating = Avg('overall'))
    div_results = div_results.annotate(avg_pay = Avg('pay'))
    div_results = div_results.annotate(avg_hours = Avg('hours'))
    div_results = div_results.annotate(avg_difficulty = Avg('difficulty'))
    
    div_results = div_results.order_by('-avg_rating')
    
    paginator = Paginator(div_results, 25)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        page_divisions = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_divisions = paginator.page(paginator.num_pages)
        
    context = {}
    context['divisions'] = page_divisions
    
    #cpnstruct context and template
    c = RequestContext(request, context)
    t = loader.get_template('reviews/favorites.html')
    
    return HttpResponse(t.render(c))

def save_review(request):
    t = loader.get_template('review.html')
    u = request.user
    cname = request.POST.get('company')
    c,k = Company.objects.get_or_create(name=cname)
    c.save()
    d = Division()
    d.company = c
    d.name = request.POST.get('division')
    d.save()
    dr = DivisionReview()
    dr.reviewer = u
    dr.employer = d
    dr.position_title = request.POST.get('position_title')
    dr.position_type = request.POST.get('position_type')
    dr.year_taken = request.POST.get('year_taken')
    dr.overall = request.POST.get('overall')
    dr.pay = request.POST.get('pay')
    dr.hours = request.POST.get('hours')
    dr.difficulty = request.POST.get('difficulty')
    dr.comment = request.POST.get('comment')
    dr.save()
    
    url = "/reviews/review/" + str(dr.id)
    return HttpResponseRedirect(url)