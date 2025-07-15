# Real-time Financial Data Processing Pipeline v2.0

This project demonstrates a modern real-time financial data processing pipeline using **RabbitMQ**, **Apache Flink**, **PostgreSQL**, and **Apache Superset**, all orchestrated with Docker. The pipeline fetches stock data from the Financial Modeling Prep API, processes it using stream processing, stores the processed data in PostgreSQL, and visualizes it using Superset.

## 🚀 New Tech Stack

- **Message Queue**: RabbitMQ (replacing Kafka)
- **Stream Processing**: Apache Flink (replacing Spark)
- **Database**: PostgreSQL (replacing MySQL)
- **Visualization**: Apache Superset (replacing Grafana)
- **Data Producer**: FastAPI (replacing plain Python script)

## 🏗️ Project Architecture

The project consists of the following components:

### 1. **Data Producer (FastAPI + RabbitMQ)**
- FastAPI web service that fetches real-time stock data from Financial Modeling Prep API
- Publishes data to RabbitMQ queue for real-time ingestion
- Provides REST API endpoints for monitoring and control
- Supports multiple stock symbols with configurable intervals

### 2. **Message Broker (RabbitMQ)**
- Advanced message queuing protocol (AMQP) broker
- Handles message routing, persistence, and delivery guarantees
- Provides web management interface for monitoring
- Supports durable queues for data reliability

### 3. **Stream Processor (Apache Flink)**
- Distributed stream processing engine
- Consumes data from RabbitMQ queues
- Processes and transforms financial data in real-time
- Writes processed data to PostgreSQL database

### 4. **Data Storage (PostgreSQL + SQLAlchemy + Alembic)**
- Advanced open-source relational database
- SQLAlchemy ORM for type-safe database operations
- Alembic for database migrations and schema management
- Optimized schema with indexes and analytics functions
- Supports complex queries and aggregations

### 5. **Data Visualization (Apache Superset)**
- Modern business intelligence platform
- Creates interactive dashboards and charts
- Connects to PostgreSQL for real-time data visualization
- Provides advanced analytics and reporting capabilities

## 📋 Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose**
- **Financial Modeling Prep API Key**: Sign up at [Financial Modeling Prep](https://site.financialmodelingprep.com/)

## 💰 Cost Information

### **Free Components (No Cost):**
- ✅ **RabbitMQ** - Completely free and open-source
- ✅ **Apache Flink** - Completely free and open-source  
- ✅ **PostgreSQL** - Completely free and open-source
- ✅ **Apache Superset** - Completely free and open-source
- ✅ **FastAPI** - Completely free and open-source
- ✅ **Docker** - Free for personal use

### **API Usage (Potentially Paid):**
- ⚠️ **Financial Modeling Prep API** - Has free and paid tiers
  - **Free Tier**: 250 API calls per day (sufficient for testing)
  - **Paid Plans**: Start at $9.99/month for more calls
  - **Sign up**: https://site.financialmodelingprep.com/developer/docs/

**Usage Calculation:**
- With 5 stock symbols and 60-second intervals: ~7,200 calls/day
- **Recommendation**: Start with free tier for testing, upgrade for production

## 🛠️ Setup Instructions

### 1. Clone and Setup
```bash
git clone <repository-url>
cd real-time-data-processing-main
```

### 2. Environment Configuration
Copy the environment template and configure it:
```bash
# Copy the template
cp env.template .env

# Edit the .env file with your API key
nano .env  # or use your preferred editor
```

**Important**: Replace `your_financial_modeling_prep_api_key_here` in the `.env` file with your actual API key from [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/).

The template includes all necessary configuration options with helpful comments.

### 3. Start the Pipeline
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

## 🌐 Access Points

- **Data Producer API**: http://localhost:8000
  - Health check: `GET /health`
  - Fetch data: `POST /fetch-data`
  - View symbols: `GET /symbols`

- **RabbitMQ Management**: http://localhost:15672
  - Username: `admin`
  - Password: `admin123`

- **Apache Flink Dashboard**: http://localhost:8081

- **Apache Superset**: http://localhost:8080
  - Default credentials: `admin/admin`

- **PostgreSQL**: localhost:5432
  - Database: `fintech_data`
  - Username: `fintech_user`
  - Password: `fintech_pass`

## 📊 Data Flow

1. **Data Ingestion**: FastAPI service fetches stock data every 60 seconds
2. **Message Queue**: Data is published to RabbitMQ queue
3. **Stream Processing**: Flink consumes and processes messages
4. **Data Storage**: Processed data is stored in PostgreSQL
5. **Visualization**: Superset creates real-time dashboards

## 🔧 Key Features

### Enhanced Data Producer
- **FastAPI-based**: Modern async web framework
- **REST API**: Health checks and control endpoints
- **Async Processing**: Non-blocking data fetching
- **Error Handling**: Robust error recovery and logging

### Advanced Message Queue
- **RabbitMQ**: Enterprise-grade message broker
- **Durable Queues**: Message persistence and reliability
- **Management UI**: Web-based monitoring interface
- **Flexible Routing**: Support for complex message patterns

### Powerful Stream Processing
- **Apache Flink**: State-of-the-art stream processing
- **Event Time Processing**: Accurate time-based analytics
- **Fault Tolerance**: Automatic recovery from failures
- **Scalable**: Distributed processing capabilities

### Modern Database with ORM
- **PostgreSQL**: Advanced relational database
- **SQLAlchemy ORM**: Type-safe database operations
- **Alembic Migrations**: Version-controlled schema changes
- **Optimized Schema**: Indexes and analytics functions
- **ACID Compliance**: Data integrity guarantees

### Rich Visualization
- **Apache Superset**: Modern BI platform
- **Interactive Dashboards**: Real-time data visualization
- **Advanced Charts**: Multiple chart types and options
- **User Management**: Role-based access control

## 📈 Monitoring and Analytics

### Real-time Metrics
- Stock price trends over time
- Price change distributions
- Volume analysis
- Market cap tracking

### Database Analytics
```python
# Using SQLAlchemy models
from database_service import DatabaseService

db = DatabaseService()

# Get recent stock data
recent_data = db.get_recent_stock_data('AAPL', hours=24)

# Get stock statistics
stats = db.get_stock_statistics('AAPL', hours=24)

# Get all symbols
symbols = db.get_all_symbols()
```

```sql
-- Direct SQL queries
-- Recent stock data
SELECT * FROM stock_data WHERE timestamp >= NOW() - INTERVAL '24 hours';

-- Stock statistics
SELECT 
    symbol,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price,
    STDDEV(price) as volatility
FROM stock_data 
WHERE timestamp >= NOW() - INTERVAL '24 hours'
GROUP BY symbol;
```

## 🚀 Performance Optimizations

- **Connection Pooling**: Efficient database connections
- **Message Persistence**: Durable RabbitMQ queues
- **Indexed Queries**: Optimized PostgreSQL schema
- **Async Processing**: Non-blocking operations
- **Caching**: Superset query caching

## 🔒 Security Features

- **Environment Variables**: Secure configuration management
- **Database Permissions**: Restricted user access
- **API Authentication**: Secure API endpoints
- **Network Isolation**: Docker network segmentation

## 🛠️ Development

### Running Individual Components
```bash
# Data Producer only
cd data-producer
python -m uvicorn main:app --reload

# Stream Processor only
cd stream-processor
python stream_processor.py
```

### Adding New Features
- **New Data Sources**: Modify `data-producer/main.py`
- **Data Transformations**: Update `stream-processor/stream_processor.py`
- **Database Schema**: 
  - Edit `stream-processor/models.py` for SQLAlchemy models
  - Run `alembic revision --autogenerate -m "description"` for migrations
  - Run `alembic upgrade head` to apply migrations
- **Visualizations**: Configure in Superset UI


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the logs: `docker-compose logs <service-name>`
- Review the documentation
- Open an issue on GitHub
