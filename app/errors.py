"""Typed application errors with user-safe messages."""


class ResumeTailorError(Exception):
    """Base error for expected application failures."""

    user_message = "The application could not complete the requested action."


class ConfigurationError(ResumeTailorError):
    """Raised when local application configuration is invalid."""

    user_message = "The local application configuration is invalid."


class DependencyUnavailableError(ResumeTailorError):
    """Raised when a required local dependency is unavailable."""

    user_message = "A required local dependency is unavailable."


class LocalServiceUnavailableError(ResumeTailorError):
    """Raised when an explicitly configured local service cannot be reached."""

    user_message = "A required local service is unavailable."

