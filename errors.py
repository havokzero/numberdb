import logging
from termcolor import colored

def handle_error(error_message, exception=None):
    """
    Handles errors by logging them and optionally printing to the console with colors.

    Args:
        error_message (str): The error message to log.
        exception (Exception, optional): The exception object to log, if any.
    """
    if exception:
        logging.error(f"{error_message}: {str(exception)}")
    else:
        logging.error(error_message)

    print(colored(f"ERROR: {error_message}", "red"))
