class GameObjectNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ComponentNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ConstructionOrderError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)