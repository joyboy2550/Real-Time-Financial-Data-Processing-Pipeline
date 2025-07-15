# Superset configuration file
import os
from datetime import timedelta

# Database configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://fintech_user:fintech_pass@postgres:5432/fintech_data'

# Security settings
SECRET_KEY = 'your-secret-key-here-change-in-production'
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None

# Feature flags
FEATURE_FLAGS = {
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'DASHBOARD_RBAC': True,
    'ENABLE_TEMPLATE_PROCESSING': True,
}

# Cache configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
}

# Celery configuration (optional, for async tasks)
class CeleryConfig:
    broker_url = 'redis://redis:6379/0'
    imports = ('superset.sql_lab', 'superset.tasks')
    result_backend = 'redis://redis:6379/0'
    worker_prefetch_multiplier = 1
    task_acks_late = False

CELERY_CONFIG = CeleryConfig

# Time grain definitions
TIME_GRAIN_FUNCTIONS = {
    'PT1S': 'DATE_TRUNC(\'second\', {col})',
    'PT1M': 'DATE_TRUNC(\'minute\', {col})',
    'PT1H': 'DATE_TRUNC(\'hour\', {col})',
    'P1D': 'DATE_TRUNC(\'day\', {col})',
    'P1W': 'DATE_TRUNC(\'week\', {col})',
    'P1M': 'DATE_TRUNC(\'month\', {col})',
    'P1Y': 'DATE_TRUNC(\'year\', {col})',
}

# Row limit
ROW_LIMIT = 5000
VIZ_ROW_LIMIT = 10000

# Web server configuration
WEBDRIVER_BASEURL = "http://superset:8088/"
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL

# Email configuration (optional)
SMTP_HOST = 'localhost'
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = 'superset'
SMTP_PORT = 25
SMTP_PASSWORD = 'superset'
SMTP_MAIL_FROM = 'superset@superset.com'

# Logging configuration
ENABLE_TIME_ROTATE = True
TIME_ROTATE_LOG_LEVEL = 'DEBUG'
FILENAME = '/var/log/superset.log'
ROLLOVER = 'midnight'
INTERVAL = 1
MAX_BYTES = 10485760  # 10MB
BACKUP_COUNT = 5

# Custom security manager
CUSTOM_SECURITY_MANAGER = None

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True

# Add this flag for using the old (legacy) datatable
LEGACY_DATATABLE_FLAG = False

# Flask-Talisman (turned off by default)
TALISMAN_ENABLED = False
TALISMAN_CONFIG = {
    'content_security_policy': {
        'default-src': ['\'self\''],
        'img-src': ['\'self\'', 'data:', 'https:'],
        'script-src': ['\'self\''],
        'style-src': ['\'self\'', '\'unsafe-inline\''],
    }
}

# Enable/disable CSP for the UI
ENABLE_PROXY_FIX = True
PROXY_FIX_CONFIG = {
    "x_for": 1,
    "x_proto": 1,
    "x_host": 1,
    "x_port": 1,
    "x_prefix": 1,
}

# Enable feature flags
FEATURE_FLAGS = {
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'DASHBOARD_RBAC': True,
    'ENABLE_TEMPLATE_PROCESSING': True,
    'GLOBAL_ASYNC_QUERIES': True,
    'VERSIONED_EXPORT': True,
}

# Custom CSS for branding
CUSTOM_CSS = """
/* Custom CSS for fintech dashboard */
.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.chart-container {
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
"""

# Custom JavaScript
CUSTOM_JS = """
// Custom JavaScript for enhanced functionality
console.log('Superset loaded with custom configuration');
""" 