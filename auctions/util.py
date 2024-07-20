from .models import ListingInformation, Watchlist, Bid


def getCurrentBidder(listingID):
    currentBidder = None
    bids = Bid.objects.filter(listing_id = listingID)
    if not bids:
        pass
    else:
        currentBidder = bids.latest("id").bidder
    
    return currentBidder
    
def getRequestFlags(request, listingID):
    watchlisted = False
    creatorIsViewingTheList = False

    if request.user.is_authenticated:
        w = Watchlist.objects.filter(listing_id = listingID, user = request.user)

        if not w:
            watchlisted = False
        else:
            watchlisted = True

        creatorIsViewingTheList = (request.user == ListingInformation.objects.get(pk = listingID).lister)
    
    return watchlisted, creatorIsViewingTheList
