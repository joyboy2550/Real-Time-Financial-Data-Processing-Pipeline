FROM apache/flink:1.18.1

USER root

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt/flink/app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a script to run the stream processor with database migrations
RUN echo '#!/bin/bash\n\
echo "Running database migrations..."\n\
cd /opt/flink/app\n\
alembic upgrade head\n\
echo "Starting stream processor..."\n\
python3 stream_processor.py\n\
' > /opt/flink/app/run.sh && chmod +x /opt/flink/app/run.sh

CMD ["/opt/flink/app/run.sh"] 