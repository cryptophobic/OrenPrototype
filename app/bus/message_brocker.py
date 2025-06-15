from collections import deque
from dataclasses import dataclass, field
from typing import Optional

from app.config import Behaviours
from app.objects.actor.actor import Actor

class Promise:
    def __init__(self):
        self.result = None
        pass

