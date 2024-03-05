class GameObject:
    def __init__(self, coords: tuple[int, int]) -> None:
        self._coords = coords

    def get_coords(self) -> tuple[int, int]:
        return self._coords
