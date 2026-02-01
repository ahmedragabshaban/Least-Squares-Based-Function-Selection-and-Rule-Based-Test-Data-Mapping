from sqlalchemy import Column, Float, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TrainingData(Base):
    __tablename__ = 'training_data'
    x = Column(Float, primary_key=True)
    y1 = Column(Float)
    y2 = Column(Float)
    y3 = Column(Float)
    y4 = Column(Float)

class IdealFunctions(Base):
    __tablename__ = 'ideal_functions'
    x = Column(Float, primary_key=True)
    pass

class TestMapping(Base):
    __tablename__ = 'test_mapping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float)
    y = Column(Float)
    delta_y = Column(Float)
    ideal_function = Column(String)
