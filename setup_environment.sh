#!/bin/bash

# Real-time Financial Data Processing Pipeline v2.0 Setup Script
# This script sets up the development environment for the new tech stack

# Stop on the first sign of trouble
set -e

echo "🚀 Setting up Real-time Financial Data Processing Pipeline v2.0"
echo "================================================================"

# Check if Python 3.11+ is available
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.11 or higher is required. Found: $python_version"
    echo "Please upgrade Python and try again."
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Check if Docker is installed
echo "🐳 Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed."
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed."
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create virtual environment
echo "📦 Creating Python virtual environment..."
if [ -d "rtpenv" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf rtpenv
fi

python3 -m venv rtpenv
echo "✅ Virtual environment created: rtpenv"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source rtpenv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install main requirements
echo "📚 Installing main dependencies..."
pip install -r requirements.txt

# Install component-specific requirements
echo "📚 Installing data producer dependencies..."
pip install -r data-producer/requirements.txt

echo "📚 Installing stream processor dependencies..."
pip install -r stream-processor/requirements.txt

# Create .env template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env template..."
    cat > .env << EOF
# API Configuration
API_KEY=your_financial_modeling_prep_api_key_here
STOCK_SYMBOLS=AAPL,GOOGL,MSFT,TSLA,AMZN

# RabbitMQ Configuration
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=admin
RABBITMQ_PASS=admin123
QUEUE_NAME=stock_data_queue

# PostgreSQL Configuration
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=fintech_data
POSTGRES_USER=fintech_user
POSTGRES_PASSWORD=fintech_pass

# Logging
LOGGING_LEVEL=INFO
EOF
    echo "✅ .env template created"
    echo "⚠️  IMPORTANT: Please edit .env file and add your Financial Modeling Prep API key"
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p data

echo "✅ Directory structure created"

# Display setup completion
echo ""
echo "🎉 Setup completed successfully!"
echo "================================================================"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file and add your Financial Modeling Prep API key"
echo "2. Run: docker-compose up --build"
echo "3. Access the services:"
echo "   - Data Producer API: http://localhost:8000"
echo "   - RabbitMQ Management: http://localhost:15672"
echo "   - Apache Flink: http://localhost:8081"
echo "   - Apache Superset: http://localhost:8080"
echo ""
echo "📚 Documentation: README.md"
echo "🐛 For issues: Check logs with 'docker-compose logs <service-name>'"
echo ""
echo "Happy coding! 🚀"
