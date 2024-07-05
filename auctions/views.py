from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import datetime
from django.utils import timezone

from .models import User, ListingInformation, Watchlist

class ListingForm(forms.ModelForm):

    class Meta:
        labels = {
            "title":"Title",
            "description":"Description",
            "price":"Initial Bid",
            "image":"Item Image",
            "category":"Category"
        }
        model = ListingInformation
        fields = ['title', 'description', 'price', 'image', 'category']

def index(request):
    return render(request, "auctions/index.html", {
        "listings": ListingInformation.objects.filter(isListingOpen = True).all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def createlisting(request):
    if request.method == "POST":
        form  = ListingForm(request.POST, request.FILES)

        if form.is_valid():
            listinginformation = form.save(commit=False)
            listinginformation.lister = request.user
            listinginformation.save()
            return HttpResponseRedirect(reverse("auctions:index"))
        
    else:
        form = ListingForm()

    return render(request, 'auctions/createlisting.html', {
        "ListingForm": form
    })

def listing(request, listingID):
    watchlisted = False
    if request.user.is_authenticated:
        w = Watchlist.objects.filter(listing_id = listingID, user = request.user)

        if not w:
            watchlisted = False
        else:
            watchlisted = True

    return render(request, "auctions/listing.html", {
        "listing": ListingInformation.objects.get(pk = listingID),
        "watchlisted": watchlisted
    })

def watchlist(request):
    if request.method == "POST":
        pleaseWatchlist = int(request.POST["pleaseWatchlist"])
        listingID = int(request.POST["listing_id"])
        if pleaseWatchlist:
            w = Watchlist(user=request.user, listing_id = listingID)
            w.save()
        else:
            w = Watchlist.objects.filter(user=request.user, listing_id = listingID)
            w.delete()
        
        return HttpResponseRedirect(reverse("auctions:listing", args=(listingID, )))

    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(user = request.user).all()
    })