# asyncpg= asyncpg is a high-performance asynchronous PostgreSQL driver for Python, used with SQLAlchemy
# to enable non-blocking database operations in FastAPI. It allows executing queries asynchronously using
# create_async_engine for improved efficiency in web applications.

# SQLAlchemy is a Python SQL toolkit and ORM that helps interact with databases using Python code instead of raw SQL.
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# constructs a database connection URL** by specifying the dialect, driver, username, password, host,
# port, and database name in a structured way.

DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    host="localhost",
    username="postgres",
    password="gai3905",
    port=5432,
    database="store_db"
)

# creates an asynchronous database engine** that enables non-blocking connections to a database,
# typically used with `asyncpg` for PostgreSQL.
engine = create_async_engine(DATABASE_URL)

# asynchronous session factory in SQLAlchemy, binding it to the database engine. It ensures autocommit
# is disabled (explicit commits required) and autoflush is disabled (queries don’t trigger automatic
# flushes).
session = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)

# creates a Base class in SQLAlchemy, which is used to define database models (tables) as Python classes.
Base = declarative_base()

# dependency injection function used in FastAPI to manage database sessions per request. ensuring it
# remains available throughout the transaction. After the request is processed, the session is automatically
# closed to prevent connection leaks.
# def get_db():
#     db = session()
#     try:
#         yield db
#     finally:
#         db.close()


async def get_db():
    async with engine.begin() as con: # Creates an asynchronous transaction to interact with the database.
        await con.run_sync(Base.metadata.create_all) # Runs table creation asynchronously if they don’t already exist.
    db = session() # Creates a new async database session using async_sessionmaker.
    try:
        yield db # Provides the session for request processing before cleanup.
    finally:
        await db.close() # Closes the session asynchronously after the request is completed.

# yield returns the database session for use in a request but does not close the function immediately.
# After the request is done, the function continues and closes the session to clean up resources.
