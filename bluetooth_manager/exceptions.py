from typing import Optional


class BluetoothManagerError(Exception):
    """
    Custom exception for BluetoothManager errors.
    """

    def __init__(
        self,
        message: str,
        command: Optional[str] = None,
        errors: Optional[str] = None
    ):
        """
        Initialize the BluetoothManagerError.

        Args:
            message (str): The error message.
            command (Optional[str]): The command that caused the error.
            errors (Optional[str]): The error message from the command output.
        """
        super().__init__(message)
        self.message = message
        self.command = command
        self.errors = errors

    def __str__(self) -> str:
        msg = self.message + "\n"
        msg += f"Command: {self.command}, " if self.command else ""
        msg += f"Errors: {self.errors or 'No additional error details.'}"
        return msg
