from django.contrib import admin
from web.reviews.models import Company, Division, DivisionReview

admin.site.register(Company)
admin.site.register(Division)
admin.site.register(DivisionReview)