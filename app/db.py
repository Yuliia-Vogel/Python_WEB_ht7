from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


DB_URL = "postgresql://postgres:my7thhomework@localhost:5433/postgres"

# engine = create_engine(DB_URL, echo=True) # параметр echo=True, щоб виводити SQL-запити в консоль (для налагодження).
engine = create_engine(DB_URL) # прибираю параметр echo=True, тому що канал вже налагоджений, 
# і зручніше відслідковувати виведення в консолі, коли нема зайвого уже непотрібного тексту про встановлення зв"язку

DB_session = sessionmaker(bind=engine)

session = DB_session()

# Перевірка з'єднання з базою даних
# try:
#     with engine.connect() as connection:
#         print("З'єднання з базою даних успішно встановлено")
# except Exception as e:
#     print(f"Помилка з'єднання з базою даних: {e}")