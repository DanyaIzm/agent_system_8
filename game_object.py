class GameObject:
    def __init__(self, coords: tuple[int, int]) -> None:
        self._coords = coords

    def get_coords(self) -> tuple[int, int]:
        """
        Get coordinates of the object

        Returns:
            tuple[int, int]: coordinates
        """
        return self._coords
