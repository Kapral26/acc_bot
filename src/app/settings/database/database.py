"""Содержит код для настройки соединения с базой данных, включая параметры подключения и инициализацию SQLAlchemy."""

from datetime import datetime

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.app.settings.configs.settings import Settings

settings = Settings()

async_engine = create_async_engine(
    url=settings.async_database_dsn,  # dsn-url
    echo=settings.debug,  # Echo отвечает, будут ли запросы выводиться в консоль
    pool_size=5,  # Количество соединений
    max_overflow=10,  # На сколько больше соединений можно открывать
)

async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""

    # Поле для хранения даты и времени создания записи.  Автоматически заполняется при создании.
    created_at: Mapped[datetime] = (
        mapped_column(
            # При добавлении записи в таблицу, автоматически устанавливается текущее время
            default=datetime.now
        ),
    )
    # Поле для хранения даты и времени последнего обновления записи. Автоматически обновляется при каждом изменении.
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        onupdate=datetime.now,  # При обновлении записи, автоматически устанавливается текущее время
        # метод now не инициализируем, что он отрабатывал каждый раз при добавлении записи
    )

    # Количество столбцов, которые будут отображаться в методе __repr__ по умолчанию.
    repr_cols_num = 3
    # Список имен столбцов, которые всегда будут отображаться в методе __repr__, вне зависимости от repr_cols_num.
    repr_cols = tuple()

    def __repr__(self) -> str:
        """Метод для формирования строкового представления объекта."""
        # Relationships (связи с другими таблицами) не используются в repr(), т.к. могут вести к неожиданным
        # подгруздкам.
        cols = []  # Список для хранения пар "имя_столбца=значение"
        # Перебираем ключи (названия) столбцов таблицы, связанной с этим классом.
        for idx, col in enumerate(self.__table__.columns.keys()):
            # Проверяем, нужно ли добавлять текущий столбец в строку представления:
            # - если столбец указан в repr_cols, то добавляем его всегда.
            # - если столбец не указан в repr_cols, но его индекс меньше repr_cols_num, то добавляем его.
            if col in self.repr_cols or idx < self.repr_cols_num:
                # Добавляем пару "имя_столбца=значение" в список cols.
                cols.append(f"{col}={getattr(self, col)}")

        # Формируем и возвращаем строку представления в формате <ИмяКласса имя_столбца1=значение1,
        # имя_столбца2=значение2, ...>
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
