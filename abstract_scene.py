from abc import ABC, abstractmethod

from game_object import GameObject


class AbstractScene(ABC):
    @abstractmethod
    def get_agents_ate_count(self) -> int:
        """
        Get count of agents which has been eaten

        Returns:
            int: count of eaten agents
        """
        ...

    @abstractmethod
    def increment_agents_ate_count(self) -> None:
        """
        Increase amount of agents on scene by 1
        """
        ...

    @abstractmethod
    def get_ticks(self) -> int:
        """
        Get amount of ticks passed since start of program (one update call is one tick)

        Returns:
            int: amount of ticks since start of program
        """
        ...

    @abstractmethod
    def get_map(self) -> list[list[GameObject]]:
        """
        Get internal scene's map

        Returns:
            list[list[GameObject]]: map
        """
        ...

    @abstractmethod
    def is_cell_empty(self, coords: tuple[int, int]) -> bool:
        """
        Check if the cell is empty

        Args:
            coords (tuple[int, int]): coords of the cell

        Returns:
            bool: cell is empty
        """
        ...

    @abstractmethod
    def get_max_agents_level(self) -> int:
        """
        Get the max level of agents

        Returns:
            int: max agent's level
        """
        ...

    @abstractmethod
    def get_agents_count(self) -> int:
        """
        Get count of agents on scene

        Returns:
            int: count of agents
        """
        ...

    @abstractmethod
    def get_width(self) -> int:
        """
        Get map width

        Returns:
            int: width
        """
        ...

    @abstractmethod
    def get_height(self) -> int:
        """
        Get map height

        Returns:
            int: height
        """
        ...

    @abstractmethod
    def add_factory(self, factory) -> None:
        """
        Add any type of factory which will be updated before any tick

        Args:
            factory (_type_): factory to be added
        """
        ...

    @abstractmethod
    def get_spawned_from(self) -> int:
        """
        Get count of agents which has been spawned by another agent

        Returns:
            int: spawned agents from another agent
        """
        ...

    @abstractmethod
    def increment_spawned_from(self) -> None:
        """
        Increase amount of spawned agents by 1
        """
        ...

    @abstractmethod
    def add_game_object(self, game_object: GameObject, coords: tuple[int, int]) -> None:
        """
        Add game object to the map

        Args:
            game_object (GameObject): game object
            coords (tuple[int, int]): coordinates of the game object
        """
        ...

    @abstractmethod
    def remove_game_object(self, game_object: GameObject) -> None:
        """
        Remove game object from the map

        Args:
            game_object (GameObject): game object
        """
        ...

    @abstractmethod
    def move_game_object(
        self, last_coords: tuple[int, int], new_coords: tuple[int, int]
    ) -> None:
        """
        Change coords of the game object

        Args:
            last_coords (tuple[int, int]): last position of the game object in coordinates
            new_coords (tuple[int, int]): new position of the game object in coordinates
        """
        ...

    @abstractmethod
    def get_random_empty_cell(self) -> tuple[int, int] | None:
        """
        Get a random cell if there are any

        Returns:
            tuple[int, int] | None: coordinates of the empty cell or nothing
        """
        ...

    @abstractmethod
    def is_agent_near(self, coords: tuple[int, int]) -> bool:
        """
        Check if agent is near to the given coordinates

        Args:
            coords (tuple[int, int]): coordinates to check near agents

        Returns:
            bool: is any agent near to the given coordinates
        """
        ...

    @abstractmethod
    def get_agent_in_coords(self, coords: tuple[int, int]) -> GameObject | None:
        """
        Get agent on coords if there is one

        Args:
            coords (tuple[int, int]): coordinates of the agent

        Returns:
            GameObject | None: agent or nothing
        """
        ...

    @abstractmethod
    def get_nearest_food_coords_by_radius(
        self, coords_from: tuple[int, int], radius: int
    ) -> tuple[int, int] | None:
        """
        Get the nearest food by given square radius

        Args:
            coords_from (tuple[int, int]): coordinates of the square center
            radius (int): square radius

        Returns:
            tuple[int, int] | None: food or nothing
        """
        ...

    @abstractmethod
    def is_food_near_coords(self, coords: tuple[int, int]) -> bool:
        """
        Check if there is food at the given coordinates at square radius equal to 1

        Args:
            coords (tuple[int, int]): coordinates

        Returns:
            bool: is there food near coordinates
        """
        ...

    @abstractmethod
    def update(self) -> None:
        """
        Proceed and increase ticks count. Update every game object in the scene
        """
        ...
