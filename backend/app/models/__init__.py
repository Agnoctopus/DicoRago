"""
Aggregates all ORM database models
"""

from .dictionary import Example, Sense, SenseTranslation, Word
from .user import User, VocabWord

__all__ = []
__all__ += ["Word", "Sense", "SenseTranslation", "Example"]
__all__ += ["User", "VocabWord"]
