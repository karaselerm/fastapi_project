"""
Модуль с настройками окружения.
Служит для того, чтобы все настройки лежали в одном месте.
А также для того, чтобы подтягивать переменные из окружения (секретов).

Для того, чтобы переменные сюда подтянулись, нужно создать файл .env
И поместить в него переменные, которые определены в настройках (db_host, db_name).
Пример находится в файлике .env.example

ВАЖНО! файл .env не должен попадать в гит коммиты.
Он содержит анные о том как подключаться к БД и другие секреты
и может дать доступ к приложению злоумышленникам.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # for PostgreSQL
<<<<<<< HEAD
    db_host: str = "postgresql+asyncpg://postgres:asel2002@localhost:5432"
    db_name: str = "fastapi_project_db"
=======
    db_host: str 
    db_name: str 
>>>>>>> 8bae65d651510abacd8d4b66a2610f1ff9587494
    db_test_name: str = "fastapi_project_test_db"
    max_connection_count: int = 1000

    @property
    def database_url(self) -> str:
        return f"{self.db_host}/{self.db_name}"


    @property
    def database_test_url(self) -> str:
        return f"{self.db_host}/{self.db_test_name}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
