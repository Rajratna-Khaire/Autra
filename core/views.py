from django.shortcuts import render
from django.http import JsonResponse
from .models import Trade
import random
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Simulated stock data for testing
STOCK_DATA = {
    'AAPL': 173.23,
    'GOOGL': 2873.45,
    'TSLA': 750.50,
}

# Home page view
def home_view(request):
    return render(request, 'home.html')

# Dashboard showing user's trades and summary
@login_required
def dashboard_view(request):
    user_trades = Trade.objects.filter(user=request.user).order_by('-timestamp')

    total_trades = user_trades.count()
    total_investment = sum(
        trade.price * trade.quantity for trade in user_trades if trade.action == 'BUY'
    )
    total_returns = sum(
        trade.price * trade.quantity for trade in user_trades if trade.action == 'SELL'
    )
    total_profit = total_returns - total_investment

    context = {
        'trades': user_trades,
        'total_trades': total_trades,
        'total_investment': round(total_investment, 2),
        'total_profit': round(total_profit, 2),
    }

    return render(request, 'dashboard.html', context)

# View to render the trading UI
@login_required
def place_trade_view(request):
    return render(request, 'trading.html')

# API to place a trade (buy/sell)
@login_required
def place_trade(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    stock = request.POST.get('stock')
    action = request.POST.get('action')
    quantity = request.POST.get('quantity')

    if not stock or not action or not quantity or not quantity.isdigit():
        return JsonResponse({'status': 'error', 'message': 'Invalid parameters or quantity'})

    quantity = int(quantity)
    price = STOCK_DATA.get(stock.upper())

    if not price:
        return JsonResponse({'status': 'error', 'message': 'Invalid stock symbol'})

    if action not in ['BUY', 'SELL']:
        return JsonResponse({'status': 'error', 'message': 'Invalid action'})

    Trade.objects.create(
        user=request.user,
        stock_symbol=stock.upper(),
        action=action,
        quantity=quantity,
        price=price,
        timestamp=timezone.now()
    )

    return JsonResponse({'status': 'success', 'message': 'Trade placed successfully'})

# Dummy API endpoint for React test
def hello_react(request):
    return JsonResponse({'message': 'Hello from Django!'})

# Renders the frontend React app (if used)
def react_app_view(request):
    return render(request, 'frontend/index.html')

# Fetches stock data and auto-triggers SELL if SL/Target hit
@login_required
def fetch_stock_data(request):
    stock = request.GET.get('stock')
    sl = request.GET.get('sl')
    target = request.GET.get('target')

    if not stock or not sl or not target:
        return JsonResponse({'status': 'error', 'message': 'Missing parameters'})

    try:
        sl = float(sl)
        target = float(target)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'SL/Target must be numbers'})

    base_price = STOCK_DATA.get(stock.upper())
    if not base_price:
        return JsonResponse({'status': 'error', 'message': 'Invalid stock symbol'})

    # Simulate current price
    current_price = round(random.uniform(base_price * 0.95, base_price * 1.05), 2)

    action = 'Hold'
    if current_price <= sl:
        action = 'Sell due to Stop Loss'
        Trade.objects.create(
            user=request.user,
            stock_symbol=stock.upper(),
            action='SELL',
            price=current_price,
            quantity=1,
            timestamp=timezone.now()
        )
    elif current_price >= target:
        action = 'Sell due to Target Hit'
        Trade.objects.create(
            user=request.user,
            stock_symbol=stock.upper(),
            action='SELL',
            price=current_price,
            quantity=1,
            timestamp=timezone.now()
        )

    return JsonResponse({
        'status': 'success',
        'stock': stock.upper(),
        'price': current_price,
        'sl': sl,
        'target': target,
        'action': action
    })
def trading_interface(request):
    # You can pass any required context here
    return render(request, 'trading_interface.html')
    
    # AI predictions