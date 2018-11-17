class GlesysException(Exception):
    """General, unspecific GleSYS exception."""


class AuthenticationException(GlesysException):
    """An error occurred during authentication."""
