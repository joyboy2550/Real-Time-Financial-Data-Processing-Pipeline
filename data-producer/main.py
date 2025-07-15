#!/usr/bin/env python3

import asyncio
import os
import logging
import json
import time
from typing import List, Dict, Any
from datetime import datetime

import aiohttp
import pika
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Constants
API_KEY = os.getenv('API_KEY')
STOCK_SYMBOLS = os.getenv('STOCK_SYMBOLS', 'AAPL,GOOGL,MSFT').split(',')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'admin123')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'stock_data_queue')

# FastAPI app
app = FastAPI(title="Financial Data Producer", version="2.0.0")

# RabbitMQ connection
connection = None
channel = None

class StockData(BaseModel):
    symbol: str
    price: float
    change_percentage: float
    volume: int
    market_cap: float
    timestamp: datetime

class DataProducer:
    def __init__(self):
        self.session = None
        self.connection = None
        self.channel = None
        
    def setup_rabbitmq(self):
        """Setup RabbitMQ connection and channel"""
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            parameters = pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare queue
            self.channel.queue_declare(queue=QUEUE_NAME, durable=True)
            logging.info(f"Connected to RabbitMQ and declared queue: {QUEUE_NAME}")
            
        except Exception as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    async def setup_session(self):
        """Setup aiohttp session"""
        self.session = aiohttp.ClientSession()
    
    async def fetch_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Fetch stock data from Financial Modeling Prep API"""
        url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}'
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and len(data) > 0:
                        stock_info = data[0]
                        return {
                            'symbol': symbol,
                            'price': stock_info.get('price', 0.0),
                            'change_percentage': stock_info.get('changesPercentage', 0.0),
                            'volume': stock_info.get('volume', 0),
                            'market_cap': stock_info.get('marketCap', 0.0),
                            'timestamp': datetime.now().isoformat()
                        }
                else:
                    logging.error(f"API request failed for {symbol}: {response.status}")
        except Exception as e:
            logging.error(f"Error fetching data for {symbol}: {e}")
        
        return None
    
    def publish_to_rabbitmq(self, data: Dict[str, Any]):
        """Publish data to RabbitMQ queue"""
        try:
            message = json.dumps(data)
            self.channel.basic_publish(
                exchange='',
                routing_key=QUEUE_NAME,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
            logging.info(f"Published data for {data['symbol']}: {data['price']}")
        except Exception as e:
            logging.error(f"Failed to publish to RabbitMQ: {e}")
    
    async def fetch_and_publish_all(self):
        """Fetch data for all symbols and publish to RabbitMQ"""
        if not self.session:
            await self.setup_session()
        
        for symbol in STOCK_SYMBOLS:
            data = await self.fetch_stock_data(symbol)
            if data:
                self.publish_to_rabbitmq(data)
        
        # Rate limiting
        await asyncio.sleep(60)
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
        if self.connection:
            self.connection.close()

# Global producer instance
producer = DataProducer()

@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup"""
    producer.setup_rabbitmq()
    await producer.setup_session()
    logging.info("Data Producer started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await producer.cleanup()
    logging.info("Data Producer shutdown complete")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Data Producer is running", "version": "2.0.0"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "rabbitmq_connected": producer.connection is not None,
        "symbols": STOCK_SYMBOLS,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/fetch-data")
async def fetch_data(background_tasks: BackgroundTasks):
    """Trigger immediate data fetch"""
    background_tasks.add_task(producer.fetch_and_publish_all)
    return {"message": "Data fetch initiated", "symbols": STOCK_SYMBOLS}

@app.get("/symbols")
async def get_symbols():
    """Get configured stock symbols"""
    return {"symbols": STOCK_SYMBOLS}

# Background task for continuous data fetching
async def continuous_data_fetch():
    """Background task that continuously fetches and publishes data"""
    while True:
        try:
            await producer.fetch_and_publish_all()
        except Exception as e:
            logging.error(f"Error in continuous data fetch: {e}")
            await asyncio.sleep(10)

@app.on_event("startup")
async def start_background_tasks():
    """Start background tasks"""
    asyncio.create_task(continuous_data_fetch()) 