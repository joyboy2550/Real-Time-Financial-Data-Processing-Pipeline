#!/usr/bin/env python3

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models import StockData, StockAnalytics, create_engine_and_session

class DatabaseService:
    """Service class for database operations using SQLAlchemy"""
    
    def __init__(self):
        self.engine, self.SessionLocal = create_engine_and_session()
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    def add_stock_data(self, data: Dict[str, Any]) -> StockData:
        """Add stock data to the database"""
        session = self.get_session()
        try:
            stock_data = StockData(
                symbol=data.get('symbol'),
                price=data.get('price', 0.0),
                change_percentage=data.get('change_percentage', 0.0),
                volume=data.get('volume', 0),
                market_cap=data.get('market_cap', 0.0),
                timestamp=data.get('timestamp', datetime.utcnow()),
                processed_at=datetime.utcnow(),
                open_price=data.get('open'),
                high_price=data.get('high'),
                low_price=data.get('low'),
                previous_close=data.get('previousClose'),
                exchange=data.get('exchange'),
                company_name=data.get('name')
            )
            
            session.add(stock_data)
            session.commit()
            session.refresh(stock_data)
            
            logging.info(f"Added stock data for {stock_data.symbol}: ${stock_data.price}")
            return stock_data
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error adding stock data: {e}")
            raise
        finally:
            session.close()
    
    def get_recent_stock_data(self, symbol: str, hours: int = 24) -> List[StockData]:
        """Get recent stock data for a symbol"""
        session = self.get_session()
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            data = session.query(StockData).filter(
                StockData.symbol == symbol,
                StockData.timestamp >= cutoff_time
            ).order_by(desc(StockData.timestamp)).all()
            
            return data
            
        except Exception as e:
            logging.error(f"Error getting recent stock data: {e}")
            raise
        finally:
            session.close()
    
    def get_stock_statistics(self, symbol: str, hours: int = 24) -> Dict[str, Any]:
        """Get stock statistics for a symbol"""
        session = self.get_session()
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            stats = session.query(
                func.avg(StockData.price).label('avg_price'),
                func.min(StockData.price).label('min_price'),
                func.max(StockData.price).label('max_price'),
                func.stddev(StockData.price).label('price_volatility'),
                func.sum(StockData.volume).label('total_volume')
            ).filter(
                StockData.symbol == symbol,
                StockData.timestamp >= cutoff_time
            ).first()
            
            if stats:
                return {
                    'symbol': symbol,
                    'avg_price': float(stats.avg_price) if stats.avg_price else 0.0,
                    'min_price': float(stats.min_price) if stats.min_price else 0.0,
                    'max_price': float(stats.max_price) if stats.max_price else 0.0,
                    'price_volatility': float(stats.price_volatility) if stats.price_volatility else 0.0,
                    'total_volume': int(stats.total_volume) if stats.total_volume else 0
                }
            else:
                return {
                    'symbol': symbol,
                    'avg_price': 0.0,
                    'min_price': 0.0,
                    'max_price': 0.0,
                    'price_volatility': 0.0,
                    'total_volume': 0
                }
                
        except Exception as e:
            logging.error(f"Error getting stock statistics: {e}")
            raise
        finally:
            session.close()
    
    def create_daily_analytics(self, symbol: str, date: datetime) -> StockAnalytics:
        """Create daily analytics for a symbol"""
        session = self.get_session()
        try:
            # Get data for the specific date
            start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            
            stats = session.query(
                func.avg(StockData.price).label('avg_price'),
                func.min(StockData.price).label('min_price'),
                func.max(StockData.price).label('max_price'),
                func.stddev(StockData.price).label('price_volatility'),
                func.sum(StockData.volume).label('total_volume')
            ).filter(
                StockData.symbol == symbol,
                StockData.timestamp >= start_date,
                StockData.timestamp < end_date
            ).first()
            
            if stats and stats.avg_price:
                analytics = StockAnalytics(
                    symbol=symbol,
                    date=start_date,
                    avg_price=float(stats.avg_price),
                    min_price=float(stats.min_price) if stats.min_price else 0.0,
                    max_price=float(stats.max_price) if stats.max_price else 0.0,
                    price_volatility=float(stats.price_volatility) if stats.price_volatility else 0.0,
                    total_volume=int(stats.total_volume) if stats.total_volume else 0,
                    created_at=datetime.utcnow()
                )
                
                session.add(analytics)
                session.commit()
                session.refresh(analytics)
                
                logging.info(f"Created daily analytics for {symbol} on {start_date.date()}")
                return analytics
            else:
                logging.warning(f"No data found for {symbol} on {start_date.date()}")
                return None
                
        except Exception as e:
            session.rollback()
            logging.error(f"Error creating daily analytics: {e}")
            raise
        finally:
            session.close()
    
    def get_all_symbols(self) -> List[str]:
        """Get all unique symbols in the database"""
        session = self.get_session()
        try:
            symbols = session.query(StockData.symbol).distinct().all()
            return [symbol[0] for symbol in symbols]
            
        except Exception as e:
            logging.error(f"Error getting symbols: {e}")
            raise
        finally:
            session.close()
    
    def cleanup_old_data(self, days: int = 30) -> int:
        """Clean up old data (older than specified days)"""
        session = self.get_session()
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            deleted_count = session.query(StockData).filter(
                StockData.timestamp < cutoff_date
            ).delete()
            
            session.commit()
            logging.info(f"Cleaned up {deleted_count} old records")
            return deleted_count
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error cleaning up old data: {e}")
            raise
        finally:
            session.close()
    
    def dispose(self):
        """Dispose of the database engine"""
        if self.engine:
            self.engine.dispose() 