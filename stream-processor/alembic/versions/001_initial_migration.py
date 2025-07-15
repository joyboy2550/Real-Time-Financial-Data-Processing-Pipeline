"""Initial migration

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create stock_data table
    op.create_table('stock_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('change_percentage', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('volume', sa.Integer(), nullable=True),
        sa.Column('market_cap', sa.Numeric(precision=20, scale=2), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('open_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('high_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('low_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('previous_close', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('exchange', sa.String(length=20), nullable=True),
        sa.Column('company_name', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create stock_analytics table
    op.create_table('stock_analytics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('avg_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('min_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('max_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('price_volatility', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('total_volume', sa.Integer(), nullable=True),
        sa.Column('price_change', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('percent_change', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for better performance
    op.create_index(op.f('ix_stock_data_symbol'), 'stock_data', ['symbol'], unique=False)
    op.create_index(op.f('ix_stock_data_timestamp'), 'stock_data', ['timestamp'], unique=False)
    op.create_index('idx_stock_data_symbol_timestamp', 'stock_data', ['symbol', 'timestamp'], unique=False)
    
    op.create_index(op.f('ix_stock_analytics_symbol'), 'stock_analytics', ['symbol'], unique=False)
    op.create_index(op.f('ix_stock_analytics_date'), 'stock_analytics', ['date'], unique=False)
    op.create_index('idx_stock_analytics_symbol_date', 'stock_analytics', ['symbol', 'date'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_stock_analytics_symbol_date', table_name='stock_analytics')
    op.drop_index(op.f('ix_stock_analytics_date'), table_name='stock_analytics')
    op.drop_index(op.f('ix_stock_analytics_symbol'), table_name='stock_analytics')
    
    op.drop_index('idx_stock_data_symbol_timestamp', table_name='stock_data')
    op.drop_index(op.f('ix_stock_data_timestamp'), table_name='stock_data')
    op.drop_index(op.f('ix_stock_data_symbol'), table_name='stock_data')
    
    # Drop tables
    op.drop_table('stock_analytics')
    op.drop_table('stock_data') 