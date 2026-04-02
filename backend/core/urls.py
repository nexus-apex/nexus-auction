from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('auctionitems/', views.auctionitem_list, name='auctionitem_list'),
    path('auctionitems/create/', views.auctionitem_create, name='auctionitem_create'),
    path('auctionitems/<int:pk>/edit/', views.auctionitem_edit, name='auctionitem_edit'),
    path('auctionitems/<int:pk>/delete/', views.auctionitem_delete, name='auctionitem_delete'),
    path('bids/', views.bid_list, name='bid_list'),
    path('bids/create/', views.bid_create, name='bid_create'),
    path('bids/<int:pk>/edit/', views.bid_edit, name='bid_edit'),
    path('bids/<int:pk>/delete/', views.bid_delete, name='bid_delete'),
    path('auctions/', views.auction_list, name='auction_list'),
    path('auctions/create/', views.auction_create, name='auction_create'),
    path('auctions/<int:pk>/edit/', views.auction_edit, name='auction_edit'),
    path('auctions/<int:pk>/delete/', views.auction_delete, name='auction_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
