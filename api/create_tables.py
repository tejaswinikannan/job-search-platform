from app.database import Base, engine
from app import models  # noqa: F401 -- import registers Company and Job on Base.metadata

Base.metadata.create_all(bind=engine)
