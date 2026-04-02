import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import AuctionItem, Bid, Auction


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['auctionitem_count'] = AuctionItem.objects.count()
    ctx['auctionitem_upcoming'] = AuctionItem.objects.filter(status='upcoming').count()
    ctx['auctionitem_live'] = AuctionItem.objects.filter(status='live').count()
    ctx['auctionitem_sold'] = AuctionItem.objects.filter(status='sold').count()
    ctx['auctionitem_total_starting_price'] = AuctionItem.objects.aggregate(t=Sum('starting_price'))['t'] or 0
    ctx['bid_count'] = Bid.objects.count()
    ctx['bid_active'] = Bid.objects.filter(status='active').count()
    ctx['bid_outbid'] = Bid.objects.filter(status='outbid').count()
    ctx['bid_won'] = Bid.objects.filter(status='won').count()
    ctx['bid_total_amount'] = Bid.objects.aggregate(t=Sum('amount'))['t'] or 0
    ctx['auction_count'] = Auction.objects.count()
    ctx['auction_english'] = Auction.objects.filter(auction_type='english').count()
    ctx['auction_dutch'] = Auction.objects.filter(auction_type='dutch').count()
    ctx['auction_sealed'] = Auction.objects.filter(auction_type='sealed').count()
    ctx['recent'] = AuctionItem.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def auctionitem_list(request):
    qs = AuctionItem.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'auctionitem_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def auctionitem_create(request):
    if request.method == 'POST':
        obj = AuctionItem()
        obj.title = request.POST.get('title', '')
        obj.category = request.POST.get('category', '')
        obj.starting_price = request.POST.get('starting_price') or 0
        obj.current_bid = request.POST.get('current_bid') or 0
        obj.bids_count = request.POST.get('bids_count') or 0
        obj.status = request.POST.get('status', '')
        obj.start_time = request.POST.get('start_time') or None
        obj.end_time = request.POST.get('end_time') or None
        obj.seller = request.POST.get('seller', '')
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/auctionitems/')
    return render(request, 'auctionitem_form.html', {'editing': False})


@login_required
def auctionitem_edit(request, pk):
    obj = get_object_or_404(AuctionItem, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.category = request.POST.get('category', '')
        obj.starting_price = request.POST.get('starting_price') or 0
        obj.current_bid = request.POST.get('current_bid') or 0
        obj.bids_count = request.POST.get('bids_count') or 0
        obj.status = request.POST.get('status', '')
        obj.start_time = request.POST.get('start_time') or None
        obj.end_time = request.POST.get('end_time') or None
        obj.seller = request.POST.get('seller', '')
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/auctionitems/')
    return render(request, 'auctionitem_form.html', {'record': obj, 'editing': True})


@login_required
def auctionitem_delete(request, pk):
    obj = get_object_or_404(AuctionItem, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/auctionitems/')


@login_required
def bid_list(request):
    qs = Bid.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(item_title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'bid_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def bid_create(request):
    if request.method == 'POST':
        obj = Bid()
        obj.item_title = request.POST.get('item_title', '')
        obj.bidder_name = request.POST.get('bidder_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.bid_time = request.POST.get('bid_time') or None
        obj.status = request.POST.get('status', '')
        obj.auto_bid = request.POST.get('auto_bid') == 'on'
        obj.max_amount = request.POST.get('max_amount') or 0
        obj.save()
        return redirect('/bids/')
    return render(request, 'bid_form.html', {'editing': False})


@login_required
def bid_edit(request, pk):
    obj = get_object_or_404(Bid, pk=pk)
    if request.method == 'POST':
        obj.item_title = request.POST.get('item_title', '')
        obj.bidder_name = request.POST.get('bidder_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.bid_time = request.POST.get('bid_time') or None
        obj.status = request.POST.get('status', '')
        obj.auto_bid = request.POST.get('auto_bid') == 'on'
        obj.max_amount = request.POST.get('max_amount') or 0
        obj.save()
        return redirect('/bids/')
    return render(request, 'bid_form.html', {'record': obj, 'editing': True})


@login_required
def bid_delete(request, pk):
    obj = get_object_or_404(Bid, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/bids/')


@login_required
def auction_list(request):
    qs = Auction.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(auction_type=status_filter)
    return render(request, 'auction_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def auction_create(request):
    if request.method == 'POST':
        obj = Auction()
        obj.title = request.POST.get('title', '')
        obj.auction_type = request.POST.get('auction_type', '')
        obj.items_count = request.POST.get('items_count') or 0
        obj.status = request.POST.get('status', '')
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/auctions/')
    return render(request, 'auction_form.html', {'editing': False})


@login_required
def auction_edit(request, pk):
    obj = get_object_or_404(Auction, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.auction_type = request.POST.get('auction_type', '')
        obj.items_count = request.POST.get('items_count') or 0
        obj.status = request.POST.get('status', '')
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/auctions/')
    return render(request, 'auction_form.html', {'record': obj, 'editing': True})


@login_required
def auction_delete(request, pk):
    obj = get_object_or_404(Auction, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/auctions/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['auctionitem_count'] = AuctionItem.objects.count()
    data['bid_count'] = Bid.objects.count()
    data['auction_count'] = Auction.objects.count()
    return JsonResponse(data)
