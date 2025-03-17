from .database import engine
from .models import Base

# Create all tables
Base.metadata.create_all(bind=engine)
# command to run python -m app.init_db
print("Tables created successfully!")
