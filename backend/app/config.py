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

    DATABASE_URL: str

    class Config:
        """
        Configuration for the Settings class.
        """

        env_file = ".env"
        case_sensitive = True


# Instantiate the settings to be used throughout the application.
settings = Settings()
