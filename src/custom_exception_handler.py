from rest_framework.views import exception_handler

def no_logging_exception_handler(exc, context):
    """
    A custom exception handler that bypasses any logging.
    It simply calls DRF's default exception handler without triggering LogModel.
    """
    return exception_handler(exc, context)
