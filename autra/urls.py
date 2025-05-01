from django.contrib import admin
from django.urls import path, re_path, include
from core import views
from core.views import (
    home_view,
    dashboard_view,
    react_app_view,
    fetch_stock_data,
    place_trade,
    place_trade_view,
    trading_interface,
)
from rest_framework_simplejwt import views as jwt_views
from django.views.generic import TemplateView
from django.views.static import serve  # Optional: to serve favicon or static fallback

urlpatterns = [
    # Admin and Auth
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    # Core Pages
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('trading/', place_trade_view, name='trading_page'),

    # API Endpoints
    path('fetch-stock/', fetch_stock_data, name='fetch_stock'),
    path('place-trade/', place_trade, name='place_trade'),

    # JWT Authentication
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # React Frontend Entry (used if you're embedding React)
    path('react/', react_app_view, name='react_app'),

    # Optional: Serve favicon.ico to prevent error in dev
    path('favicon.ico', serve, {'path': 'favicon.ico', 'document_root': 'static'}),
    path('trading/', views.trading_interface, name='trading_interface'),

    # Catch-all for React Router paths (this should always be last)
    re_path(r'^(?!admin|accounts|api|place-trade|fetch-stock|dashboard|trading|react)(?P<path>.*)/?$', react_app_view),
]
