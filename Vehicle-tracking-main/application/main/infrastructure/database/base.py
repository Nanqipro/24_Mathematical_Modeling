from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from util.common import read_db_config

Base = declarative_base()
_engine = None
_SessionFactory = None


def session_factory():
    global _engine, _SessionFactory
    if _SessionFactory is None:
        project_root = Path(__file__).resolve().parents[4]
        connection_string = read_db_config(
            config_path=project_root / "settings" / "db_config.yml"
        )
        _engine = create_engine(connection_string)
        _SessionFactory = sessionmaker(bind=_engine)

    Base.metadata.create_all(_engine)
    return _SessionFactory()
