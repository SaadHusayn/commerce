from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(ListingInformation)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)