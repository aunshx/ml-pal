from user import Base, engine

Base.metadata.create_all(bind=engine)
