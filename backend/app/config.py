"""
Module for application configuration settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings.

    Attributes:
        DATABASE_URL (str): The URL of the database.
    """

    APP_NAME: str = "DicoRago"

    # Databases
    DATABASE_MAIN_URL: str
    DATABASE_DICT_URL: str

    # Auth
    GOOGLE_CLIENT_ID: str
    APPLE_CLIENT_ID: str
    AUTH_SECRET: str

    class Config:
        """
        Configuration for the Settings class.
        """

        env_file = ".env"
        case_sensitive = True


# Instantiate the settings to be used throughout the application.
settings = Settings()
