from app.collections.name_repository import name_repository


class Component:
    def __init__(self, name: str = None):
        _id = name_repository.get_name(name)
        self._id: str = _id

    @property
    def id(self) -> str:
        return self._id
