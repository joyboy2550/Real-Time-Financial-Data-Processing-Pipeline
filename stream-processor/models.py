#!/usr/bin/env python3

from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create base class for models
Base = declarative_base()

class StockData(Base):
    """SQLAlchemy model for stock data"""
    __tablename__ = 'stock_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    change_percentage = Column(Numeric(5, 2))
    volume = Column(Integer)
    market_cap = Column(Numeric(20, 2))
    timestamp = Column(DateTime, nullable=False, index=True)
    processed_at = Column(DateTime, default=datetime.utcnow)
    
    # Additional fields for enhanced analytics
    open_price = Column(Numeric(10, 2))
    high_price = Column(Numeric(10, 2))
    low_price = Column(Numeric(10, 2))
    previous_close = Column(Numeric(10, 2))
    exchange = Column(String(20))
    company_name = Column(String(100))
    
    # Define composite index
    __table_args__ = (
        Index('idx_stock_data_symbol_timestamp', 'symbol', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<StockData(symbol='{self.symbol}', price={self.price}, timestamp='{self.timestamp}')>"

class StockAnalytics(Base):
    """SQLAlchemy model for computed stock analytics"""
    __tablename__ = 'stock_analytics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    avg_price = Column(Numeric(10, 2))
    min_price = Column(Numeric(10, 2))
    max_price = Column(Numeric(10, 2))
    price_volatility = Column(Numeric(10, 4))
    total_volume = Column(Integer)
    price_change = Column(Numeric(10, 2))
    percent_change = Column(Numeric(5, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Define composite index
    __table_args__ = (
        Index('idx_stock_analytics_symbol_date', 'symbol', 'date'),
    )
    
    def __repr__(self):
        return f"<StockAnalytics(symbol='{self.symbol}', date='{self.date}', avg_price={self.avg_price})>"

def get_database_url():
    """Get database URL from environment variables"""
    host = os.getenv('POSTGRES_HOST', 'postgres')
    port = os.getenv('POSTGRES_PORT', '5432')
    database = os.getenv('POSTGRES_DB', 'fintech_data')
    user = os.getenv('POSTGRES_USER', 'fintech_user')
    password = os.getenv('POSTGRES_PASSWORD', 'fintech_pass')
    
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def create_engine_and_session():
    """Create SQLAlchemy engine and session"""
    database_url = get_database_url()
    engine = create_engine(database_url, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal

def create_tables(engine):
    """Create all tables"""
    Base.metadata.create_all(bind=engine) 