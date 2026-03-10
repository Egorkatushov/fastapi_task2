from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os


class Database:
    def __init__(self):
        # Путь к базе данных в корне проекта
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        db_path = os.path.join(base_dir, 'db.sqlite3')
        self._db_url = f"sqlite:///{db_path}"
        print(f"Подключение к БД: {self._db_url}")  # Для отладки
        self._engine = create_engine(self._db_url, echo=False)

    @contextmanager
    def session(self):
        connection = self._engine.connect()
        Session = sessionmaker(bind=self._engine)
        session = Session()

        try:
            yield session
            session.commit()
            connection.close()
        except Exception:
            session.rollback()
            raise


database = Database()
Base = declarative_base()