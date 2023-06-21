from pathlib import Path

from sqlalchemy import create_engine

db_path = Path(__file__).resolve().absolute().parent.parent / "main.db"
engine = create_engine(f"sqlite:///" + str(db_path))
