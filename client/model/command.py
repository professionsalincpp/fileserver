from abc import ABC, abstractmethod
from typing import Any

class Command(ABC):
    """Command interface."""
    @abstractmethod
    def execute(self) -> Any:
        """Execute the command."""
        ...