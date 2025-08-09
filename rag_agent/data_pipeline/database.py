import os
from sqlalchemy import create_engine

def get_db_engine(db_path="data/tickets.db"):
    # Ensure the directory for the database exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connection string points to a file path.
    engine = create_engine(f'sqlite:///{db_path}')
    return engine