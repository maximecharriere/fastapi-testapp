from sqlalchemy import Column, Integer, Float
from app.database import Base, engine

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    revenue = Column(Float, nullable=False)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)