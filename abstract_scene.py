from abc import ABC, abstractmethod

from game_object import GameObject


class AbstractScene(ABC):
    @abstractmethod
    def get_agents_ate_count(self) -> int: ...

    @abstractmethod
    def increment_agents_ate_count(self) -> None: ...

    @abstractmethod
    def get_ticks(self) -> int: ...

    @abstractmethod
    def get_map(self) -> list[list[GameObject]]: ...

    @abstractmethod
    def is_cell_empty(self, coords: tuple[int, int]) -> bool: ...

    @abstractmethod
    def get_max_agents_level(self) -> int: ...

    @abstractmethod
    def get_agents_count(self) -> int: ...

    @abstractmethod
    def get_width(self) -> int: ...

    @abstractmethod
    def get_height(self) -> int: ...

    @abstractmethod
    def add_factory(self, factory) -> None: ...

    @abstractmethod
    def get_spawned_from(self) -> int: ...

    @abstractmethod
    def increment_spawned_from(self) -> None: ...

    @abstractmethod
    def add_game_object(
        self, game_object: GameObject, coords: tuple[int, int]
    ) -> None: ...

    @abstractmethod
    def remove_game_object(self, game_object: GameObject) -> None: ...

    @abstractmethod
    def move_game_object(
        self, last_coords: tuple[int, int], new_coords: tuple[int, int]
    ) -> None: ...

    @abstractmethod
    def get_random_empty_cell(self) -> tuple[int, int] | None: ...

    @abstractmethod
    def is_agent_near(self, coords: tuple[int, int]) -> bool: ...

    @abstractmethod
    def get_agent_in_coords(self, coords: tuple[int, int]) -> GameObject | None: ...

    @abstractmethod
    def get_nearest_food_coords_by_radius(
        self, coords_from: tuple[int, int], radius: int
    ) -> tuple[int, int] | None: ...

    @abstractmethod
    def is_food_near_coords(self, coords: tuple[int, int]) -> bool: ...

    @abstractmethod
    def update(self) -> None: ...
