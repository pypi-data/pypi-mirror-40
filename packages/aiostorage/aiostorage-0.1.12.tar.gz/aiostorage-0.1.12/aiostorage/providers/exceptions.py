"""
This module contains exceptions for object storage provider API errors.
"""


class ProviderError(Exception):
    """
    Base exception class.
    """


class ProviderAuthenticationError(ProviderError):
    """
    Unable to authenticate.
    """


class ProviderGetUploadUrlError(ProviderError):
    """
    Unable to get file upload URL.
    """


class ProviderAuthorizationError(ProviderError):
    """
    Unable to perform action due to lack of authorization.
    """


class ProviderFileUploadError(ProviderError):
    """
    Unable to upload file.
    """
