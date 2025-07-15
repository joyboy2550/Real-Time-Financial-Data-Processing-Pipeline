#!/usr/bin/env python3

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any

import pika
from dotenv import load_dotenv
from database_service import DatabaseService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Constants
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'admin123')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'stock_data_queue')

class StreamProcessor:
    def __init__(self):
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None
        self.db_service = None
        
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
            
            self.rabbitmq_connection = pika.BlockingConnection(parameters)
            self.rabbitmq_channel = self.rabbitmq_connection.channel()
            
            # Declare queue
            self.rabbitmq_channel.queue_declare(queue=QUEUE_NAME, durable=True)
            logging.info(f"Connected to RabbitMQ and declared queue: {QUEUE_NAME}")
            
        except Exception as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    def setup_database(self):
        """Setup database service"""
        try:
            self.db_service = DatabaseService()
            logging.info("Connected to PostgreSQL database via SQLAlchemy")
            
        except Exception as e:
            logging.error(f"Failed to connect to PostgreSQL: {e}")
            raise
    
    def process_message(self, ch, method, properties, body):
        """Process incoming message from RabbitMQ using SQLAlchemy"""
        try:
            # Parse JSON message
            data = json.loads(body.decode('utf-8'))
            
            # Parse timestamp
            timestamp_str = data.get('timestamp')
            if timestamp_str:
                data['timestamp'] = datetime.fromisoformat(timestamp_str)
            else:
                data['timestamp'] = datetime.utcnow()
            
            # Add stock data to database
            stock_data = self.db_service.add_stock_data(data)
            
            logging.info(f"Processed data for {stock_data.symbol}: Price=${stock_data.price}, Change={stock_data.change_percentage}%")
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            # Reject message and requeue
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def start_processing(self):
        """Start consuming messages from RabbitMQ"""
        try:
            # Setup connections
            self.setup_rabbitmq()
            self.setup_database()
            
            # Set QoS
            self.rabbitmq_channel.basic_qos(prefetch_count=1)
            
            # Start consuming
            self.rabbitmq_channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=self.process_message
            )
            
            logging.info("Starting to consume messages from RabbitMQ...")
            self.rabbitmq_channel.start_consuming()
            
        except KeyboardInterrupt:
            logging.info("Stopping stream processor...")
        except Exception as e:
            logging.error(f"Error in stream processing: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup connections"""
        try:
            if self.rabbitmq_connection:
                self.rabbitmq_connection.close()
            if self.db_service:
                self.db_service.dispose()
            logging.info("Connections closed")
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

def main():
    """Main function"""
    processor = StreamProcessor()
    processor.start_processing()

if __name__ == "__main__":
    main() 