from sqlalchemy import create_engine
# from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
SUPABASE_USER = os.getenv('SUPABASE_USER')
SUPABASE_PASSWORD = os.getenv('SUPABASE_PASSWORD')
SUPABASE_HOST = os.getenv('SUPABASE_HOST')
SUPABASE_PORT = os.getenv('SUPABASE_PORT')
SUPABASE_DB = os.getenv('SUPABASE_DB')

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_HOST}:{SUPABASE_PORT}/{SUPABASE_DB}"

print(DATABASE_URL)

# Create the SQLAlchemy engine
engine = create_engine('postgresql://semen:58b5WOGgBk88efEcjJhfuH11yxlHpmnd@dpg-d2ade47diees738tsl80-a.oregon-postgres.render.com/betka')
# If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
# https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
# engine = create_engine(DATABASE_URL, poolclass=NullPool)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")