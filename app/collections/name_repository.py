from app.core.unique_name import generate_unique_name


class NameRepository:
    def __init__(self):
        self.names: set[str] = set()

    def get_name(self, name: str = None) -> str:
        if name is None or name in self.names:
            name = generate_unique_name(self.names)
        self.names.add(name)

        return name

name_repository = NameRepository()