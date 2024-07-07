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
    path("listing/<int:listingID>", views.listing, name="listing"),
    path("bid", views.bid, name="bid")
]
