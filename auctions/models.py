from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    def __str__(self):
        return self.username
    
    

class ListingInformation(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=200)
    bidCurrentPrice = models.FloatField()
    image = models.ImageField(blank=True, upload_to="auctions/images/")
    category = models.CharField(max_length=64, blank=True, null=True)
    lister = models.ForeignKey(User, on_delete=models.CASCADE , related_name="listings")
    time = models.DateTimeField(auto_now_add=True)
    isListingOpen = models.BooleanField(default=True)
    winner =  models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.title} listed by {self.lister}"


class Comment(models.Model):
    content = models.CharField(max_length=120)
    writer = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="comments")
    listing = models.ForeignKey(ListingInformation, on_delete=models.CASCADE, related_name="comments")
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.writer}: {self.content}"



class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddings")
    listing = models.ForeignKey(ListingInformation, on_delete=models.CASCADE, related_name="bids")
    bidPrice = models.FloatField()

    def __str__(self):
        return f"Bid of {self.bidPrice} by {self.bidder} on {self.listing}"
    
class Watchlist(models.Model):
    listing = models.ForeignKey(ListingInformation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"Listing: {self.listing}, watchlisted by {self.user}"