import os
import datetime
from typing import Optional

class Debug:
    _enabled: bool = False
    
    @classmethod
    def enable(cls):
        cls._enabled = True
    
    @classmethod
    def disable(cls):
        cls._enabled = False
    
    @classmethod
    def is_enabled(cls) -> bool:
        return cls._enabled
    
    @classmethod
    def log(cls, message: str, filename: Optional[str] = None):
        if not cls._enabled:
            return
            
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        if filename:
            base_filename = os.path.basename(filename)
            print(f"[{timestamp}] [{base_filename}] {message}")
        else:
            print(f"[{timestamp}] {message}")