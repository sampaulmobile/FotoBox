from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin

# Enables the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # link to the resources files
    (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    
    #mainpage
    (r'^$', 'reviews.views.index'),
    
    #reviews
	(r'^fotobox/$', 'profiles.views.fotobox'),
    (r'^reviews/$', 'reviews.views.index'),
    (r'^reviews/recommended$', 'reviews.views.index'),
    (r'^reviews/review/(\d+)', 'reviews.views.review'),
    (r'^save_review/', 'reviews.views.save_review'),
    (r'^create_review/', 'reviews.views.create_review'),
    (r'^reviews/mine/', 'reviews.views.my_reviews'),
	
	#Favorites
    (r'^favorites/', 'reviews.views.list_favorites'),
    (r'^profiles/toggle_favorite', 'profiles.views.toggle_favorite'),
	
    #other pages
    (r'^accounts/', include('registration.urls')),
	(r'^account_info/', 'profiles.views.account_info'),
	(r'^account_update/', 'profiles.views.account_update'),
	(r'^search/', 'reviews.views.search_reviews'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #Admin Site
    url(r'^admin/', include(admin.site.urls)),
)