from src.config import config


db_config = {
    "connections": {
        "default": config.database.url
    },
    "apps": {
        "models": {
            "models": ["src.database.models"],
            "default_connection": "default",
        }
    },
}
