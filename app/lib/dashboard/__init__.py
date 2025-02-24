from sqlalchemy import MetaData, Table, create_engine

DB_USER = 'koalaty'
DB_PASSWORD = 'eucalyptus'
DB_HOST = '127.0.0.1'
DB_PORT = 3307
DB_NAME = 'koalaty'
# DB_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 280,
    'pool_size': 10,       # Number of connections to keep open inside the pool
    'max_overflow': 20    # Additional connections allowed above pool_size
}

engine = create_engine(DB_URL, **SQLALCHEMY_ENGINE_OPTIONS)
metadata = MetaData()

OrderLineTotals = Table('order_line_totals', metadata, autoload_with=engine)
Orders = Table('orders', metadata, autoload_with=engine)
OrderLines = Table('order_lines', metadata, autoload_with=engine)
