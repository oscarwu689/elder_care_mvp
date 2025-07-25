from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://elder_care_user:ILdfo1IsAhqyXEgLxZvMYgaaDYugHTlE@dpg-d21i7j7fte5s73fkt7i0-a.virginia-postgres.render.com/elder_care",
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)