# your_app/tasks.py

from celery import shared_task
from .utils import fetch_stock_data, place_order
import logging

# Setting up a logger
logger = logging.getLogger(__name__)

@shared_task
def run_auto_trading():
    """
    Automated trading logic. It fetches stock data and places buy or sell orders based on stock price.
    This task is scheduled to run periodically via Celery Beat.
    """
    logger.info("Starting automated trading task...")

    # Fetch stock data for RELIANCE
    stock_data = fetch_stock_data("RELIANCE")
    
    if stock_data:
        logger.info(f"Fetched stock data for RELIANCE: Price = {stock_data['price']}")
        
        if stock_data['price'] < 2500:  # Buy condition
            logger.info(f"Price is below 2500, placing BUY order for 1 share.")
            place_order(symbol="RELIANCE", action="BUY", quantity=1)
        elif stock_data['price'] > 2600:  # Sell condition
            logger.info(f"Price is above 2600, placing SELL order for 1 share.")
            place_order(symbol="RELIANCE", action="SELL", quantity=1)
        else:
            logger.info("Price is in the neutral zone. No action taken.")
    else:
        logger.error("Failed to fetch stock data for RELIANCE.")
