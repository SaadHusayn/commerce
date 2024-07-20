from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ListingForm
from .models import User, ListingInformation, Watchlist, Bid, Comment
from .util import *

def index(request):
    return render(request, "auctions/index.html", {
        "listings": ListingInformation.objects.filter(isListingOpen = True).all(),
        "message": "Active Listings"
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

@login_required
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
    listingObj = ListingInformation.objects.get(pk = listingID)
    message=""
    watchlisted, creatorIsViewingTheList = getRequestFlags(request, listingID)
    


    if request.method == "POST":
        isBidingForm = int(request.POST["isBidingForm"])
        if isBidingForm:

            price = float(request.POST["bidPrice"])

            if(price <= listingObj.bidCurrentPrice):
                message = "Bid Not Placed. Bid price is less than the current price of the listing"
            else:
                listingObj.bidCurrentPrice = price
                listingObj.save()
                newBid = Bid(bidPrice = price, bidder = request.user, listing = listingObj)
                newBid.save()

        
        else:

            listingObj.isListingOpen = 0 
            listingObj.winner = getCurrentBidder(listingID)
            listingObj.save()
        

    currentBidder = getCurrentBidder(listingID)

    return render(request, "auctions/listing.html", {
        "listing": listingObj,
        "watchlisted": watchlisted,
        "creatorIsViewingTheList": creatorIsViewingTheList,
        "message":message,
        "numBids": Bid.objects.filter(listing_id = listingID).count(),
        "currentBidder": currentBidder,
        "comments": listingObj.comments.all()
    })

@login_required
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

    return render(request, "auctions/index.html", {
        "message": "Watchlist",
        "watchlist": Watchlist.objects.filter(user = request.user).all(),
        "isWatchlist": 1
    })

@login_required
def saveComment(request, listingID):
    listingObj = ListingInformation.objects.get(pk = listingID)

    if request.method == "POST":
        commentContent = request.POST["comment"]

        newComment = Comment(content = commentContent, writer = request.user, listing = listingObj)
        newComment.save()

        return HttpResponseRedirect(reverse("auctions:listing", args=(listingID, )))


def closelistings(request):
    return render(request, 'auctions/index.html', {
        "listings": ListingInformation.objects.filter(isListingOpen = False).all(),
        "message": "Close Listings"
    })

def category(request, categoryName = None):
    if not categoryName:
        categories = []
        allListingsWithCategory = ListingInformation.objects.exclude(category__isnull=True).exclude(category__exact='').filter(isListingOpen = True)
        for listing in allListingsWithCategory:
            if listing.category not in categories:
                categories.append(listing.category)
        
        return render(request, 'auctions/category.html', {
            "categories": categories
        })
    else:
        categoryListings = ListingInformation.objects.filter(category = categoryName).filter(isListingOpen = True)
        return render(request, 'auctions/index.html', {
            "message": f"Category Listing: {categoryName}",
            "listings": categoryListings
        })

def userProfile(request, username):

    user = User.objects.get(username = username)

    listings = user.listings.all()

    return render(request, 'auctions/user.html', {
        "userInfo":user,
        "activeListings":listings.filter(isListingOpen = 1),
        "closeListings":listings.filter(isListingOpen = 0)
    })