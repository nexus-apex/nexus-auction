from django.db import models

class AuctionItem(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, default="")
    starting_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_bid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bids_count = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("upcoming", "Upcoming"), ("live", "Live"), ("sold", "Sold"), ("unsold", "Unsold"), ("cancelled", "Cancelled")], default="upcoming")
    start_time = models.DateField(null=True, blank=True)
    end_time = models.DateField(null=True, blank=True)
    seller = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Bid(models.Model):
    item_title = models.CharField(max_length=255)
    bidder_name = models.CharField(max_length=255, blank=True, default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bid_time = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("outbid", "Outbid"), ("won", "Won"), ("retracted", "Retracted")], default="active")
    auto_bid = models.BooleanField(default=False)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.item_title

class Auction(models.Model):
    title = models.CharField(max_length=255)
    auction_type = models.CharField(max_length=50, choices=[("english", "English"), ("dutch", "Dutch"), ("sealed", "Sealed"), ("reserve", "Reserve")], default="english")
    items_count = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("scheduled", "Scheduled"), ("live", "Live"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="scheduled")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
