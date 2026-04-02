from django.contrib import admin
from .models import AuctionItem, Bid, Auction

@admin.register(AuctionItem)
class AuctionItemAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "starting_price", "current_bid", "bids_count", "created_at"]
    list_filter = ["status"]
    search_fields = ["title", "category", "seller"]

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ["item_title", "bidder_name", "amount", "bid_time", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["item_title", "bidder_name"]

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ["title", "auction_type", "items_count", "status", "start_date", "created_at"]
    list_filter = ["auction_type", "status"]
    search_fields = ["title"]
