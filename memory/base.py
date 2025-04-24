from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

class MemoryDriver(ABC):
    @abstractmethod
    def save(self,data:Dict[str,Any])->None:...
    
    @abstractmethod
    def load(self)->Dict[str,Any]:...