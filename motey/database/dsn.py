from motey.config import Config


def build_dsn(config: Config = Config()) -> str:
    return (
        f"mysql+pymysql://{config.database_user}"
        f":{config.database_password}"
        f"@{config.database_host}:{config.database_port}/{config.database}"
    )
