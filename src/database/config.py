from src.settings import settings

config = {
    "connections": {
        "default": f"postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@database:5432/{settings.POSTGRES_DB}"
    },
    "apps": {
        "models": {
            "models": ["src.database.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
