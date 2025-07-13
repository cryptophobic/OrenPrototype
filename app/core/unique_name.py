from typing import Set

import petname


def generate_unique_name(data: Set[str]) -> str:
    """Generate a unique name with timestamp fallback"""
    base_name = petname.Generate(2, separator="-")

    name = f"{base_name}"
    counter = 1

    if name in data:
        while f"{base_name}-{counter}" in data:
            counter += 1
        name = f"{base_name}-{counter}"

    return name
