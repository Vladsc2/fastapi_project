from pydantic_settings import BaseSettings


class _Config(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///data_base.sqlite3"
    db_echo: bool = False

    game_name: str = "Little Browser Game 1"


config = _Config()

