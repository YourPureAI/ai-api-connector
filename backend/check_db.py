from sqlalchemy import create_engine, inspect
from app.core.config import settings

def check_tables():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables found: {tables}")

if __name__ == "__main__":
    check_tables()
