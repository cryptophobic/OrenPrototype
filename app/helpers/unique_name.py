import time
from typing import Set

import petname


def generate_unique_name(data: Set[str]) -> str:
    """Generate a unique name with timestamp fallback"""
    base_name = petname.Generate(2, separator="-")

    timestamp = int(time.time() * 1000) % 10000
    name = f"{base_name}-{timestamp}"

    if name in data:
        counter = timestamp + 1
        while f"{base_name}-{counter}" in data:
            counter += 1
        name = f"{base_name}-{counter}"

    return name
