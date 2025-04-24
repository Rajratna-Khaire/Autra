from django.shortcuts import render
from django.http import JsonResponse
from .models import Trade

def home_view(request):
    return render(request, 'home.html')

def dashboard_view(request):
    user_trades = Trade.objects.filter(user=request.user).order_by('-timestamp')
    total_trades = user_trades.count()
    total_investment = sum(trade.price * trade.quantity for trade in user_trades if trade.action == 'BUY')
    total_returns = sum(trade.price * trade.quantity for trade in user_trades if trade.action == 'SELL')
    total_profit = total_returns - total_investment

    context = {
        'trades': user_trades,
        'total_trades': total_trades,
        'total_investment': round(total_investment, 2),
        'total_profit': round(total_profit, 2),
    }

    return render(request, 'dashboard.html', context)

def hello_react(request):
    return JsonResponse({'message': 'Hello from Django!'})

def react_app_view(request):
    return render(request, 'frontend/index.html')
