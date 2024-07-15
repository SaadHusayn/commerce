from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view , name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createlisting, name="createlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("closelistings", views.closelistings, name="closelistings"),
    path("listing/<int:listingID>", views.listing, name="listing"),
    path("comment/<int:listingID>", views.saveComment, name = "saveComment"),
    path("category" , views.category, name="category"),
    path("category/<str:categoryName>", views.category, name="categoryListings"),
    path("user/<str:username>", views.userProfile, name="userProfile")
    # path("bid", views.bid, name="bid")
]
