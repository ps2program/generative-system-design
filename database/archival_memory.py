from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
DATABASE = 'sqlite:///archival_memory_db.db'
engine = create_engine(DATABASE, echo=True)
Base = declarative_base()

# Define the ChatHistory model
class Archival_ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())

# Define the Requirements model
class Requirements(Base):
    __tablename__ = 'requirements'
    id = Column(Integer, primary_key=True, autoincrement=True)
    requirements_name = Column(String, nullable=False)
    requirements_json = Column(Text, nullable=False)  # JSON storage
    created_at = Column(DateTime, default=func.now())

# Define the Functions model
class Functions(Base):
    __tablename__ = 'functions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    functions_name = Column(String, nullable=False)
    functions_json = Column(Text, nullable=False)  # JSON storage
    created_at = Column(DateTime, default=func.now())

# Define the Products model
class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    products_name = Column(String, nullable=False)
    products_json = Column(Text, nullable=False)  # JSON storage
    created_at = Column(DateTime, default=func.now())

# Define the LogicalConnections model
class LogicalConnections(Base):
    __tablename__ = 'logical_connections'
    id = Column(Integer, primary_key=True, autoincrement=True)
    connection_name = Column(String, nullable=False)  # Name or description of the connection
    connection_type = Column(String, nullable=True)   # Type of the connection (optional)
    connection_json = Column(Text, nullable=False)    # JSON storage
    created_at = Column(DateTime, default=func.now())

# Create tables
Base.metadata.create_all(engine)

# Session setup
Archival_Session = sessionmaker(bind=engine)
archival_session = Archival_Session()
