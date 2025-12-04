from sqlmodel import SQLModel, create_engine, Session
from backend.app.core.config import settings
from typing import Generator

# Create the database engine
# pool_pre_ping=True helps handle DB connection drops
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=False)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.
    Yields a Session object and closes it after use.
    """
    with Session(engine) as session:
        yield session

def init_db():
    """
    Initialize the database.
    This can be used to create tables if they don't exist.
    """
    # SQLModel.metadata.create_all(engine)
    # Commented out because we are using an existing schema 
    # and should be careful about auto-creating tables.
    pass

def test_connection():
    from sqlalchemy import inspect, text
    try:
        print("Testing database connection...")
        with Session(engine) as session:
            # Try a simple query
            session.exec(text("SELECT 1"))
            print("Database connection successful!")
            
            # List tables
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"Found {len(tables)} tables:")
            for table in tables:
                print(f" - {table}")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
