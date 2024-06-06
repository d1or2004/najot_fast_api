from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Engine = create_engine('postgresql://postgres:2004@localhost/fast_ip', echo=True)

Base = declarative_base()
session = sessionmaker()


def SessionLocal():
    engine = create_engine('postgresql://postgres:2004@localhost/fast_ip', echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
