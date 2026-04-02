from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import AuctionItem, Bid, Auction
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusAuction with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusauction.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if AuctionItem.objects.count() == 0:
            for i in range(10):
                AuctionItem.objects.create(
                    title=f"Sample AuctionItem {i+1}",
                    category=f"Sample {i+1}",
                    starting_price=round(random.uniform(1000, 50000), 2),
                    current_bid=round(random.uniform(1000, 50000), 2),
                    bids_count=random.randint(1, 100),
                    status=random.choice(["upcoming", "live", "sold", "unsold", "cancelled"]),
                    start_time=date.today() - timedelta(days=random.randint(0, 90)),
                    end_time=date.today() - timedelta(days=random.randint(0, 90)),
                    seller=f"Sample {i+1}",
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 AuctionItem records created'))

        if Bid.objects.count() == 0:
            for i in range(10):
                Bid.objects.create(
                    item_title=f"Sample Bid {i+1}",
                    bidder_name=f"Sample Bid {i+1}",
                    amount=round(random.uniform(1000, 50000), 2),
                    bid_time=date.today() - timedelta(days=random.randint(0, 90)),
                    status=random.choice(["active", "outbid", "won", "retracted"]),
                    auto_bid=random.choice([True, False]),
                    max_amount=round(random.uniform(1000, 50000), 2),
                )
            self.stdout.write(self.style.SUCCESS('10 Bid records created'))

        if Auction.objects.count() == 0:
            for i in range(10):
                Auction.objects.create(
                    title=f"Sample Auction {i+1}",
                    auction_type=random.choice(["english", "dutch", "sealed", "reserve"]),
                    items_count=random.randint(1, 100),
                    status=random.choice(["scheduled", "live", "completed", "cancelled"]),
                    start_date=date.today() - timedelta(days=random.randint(0, 90)),
                    end_date=date.today() - timedelta(days=random.randint(0, 90)),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Auction records created'))
