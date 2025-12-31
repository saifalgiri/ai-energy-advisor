
class NotFoundException(Exception):
    """Exception raised when a resource is not found"""
    pass


class ValidationException(Exception):
    """Exception raised for validation errors"""
    pass


class ExternalServiceException(Exception):
    """Exception raised when an external service fails"""
    pass