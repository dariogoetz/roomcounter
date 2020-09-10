from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Room Counter"

    DB_URI: str = "sqlite:///./roomcounter.sqlite"
    INITIAL_USER: str = "dario"
    INITIAL_PASSWORD: str = "uiae"
    INITIAL_ROOM_NAME: str = "Outside"

    SECRET_KEY: str = "c902190dc53dba745b1905dcec36aec84212eaab2992ce2eff0078e5bfde0082"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
