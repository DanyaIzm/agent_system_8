from itertools import product
from random import choice

from abstract_scene import AbstractScene
from agent import Agent
from food import Food
from game_object import GameObject


def _is_in_bound(value, max_value) -> bool:
    return value >= 0 and value < max_value


class Scene(AbstractScene):
    def __init__(self) -> None:
        self._field_width = 20
        self._field_height = 20
        self._map = [
            [None for _ in range(self._field_width)] for _ in range(self._field_height)
        ]
        self._random_cell_picker = RandomCellPicker(self)
        self._factories = []
        self._agents_ate_count = 0
        self._spawned_from_count = 0
        self._ticks = 1
        self._removed = []

    def get_agents_ate_count(self) -> int:
        return self._agents_ate_count

    def increment_agents_ate_count(self) -> None:
        self._agents_ate_count += 1

    def get_ticks(self) -> int:
        return self._ticks

    def get_map(self) -> list[list[GameObject]]:
        return self._map

    def get_width(self) -> int:
        return self._field_width

    def get_height(self) -> int:
        return self._field_height

    def add_factory(self, factory) -> None:
        self._factories.append(factory)

    def get_spawned_from(self) -> int:
        return self._spawned_from_count

    def increment_spawned_from(self) -> None:
        self._spawned_from_count += 1

    def add_game_object(self, game_object, coords: tuple[int, int]) -> None:
        if not game_object:
            return

        if self._map[coords[1]][coords[0]]:
            raise ValueError("Tried to put object on the scene to not empty cell")

        self._map[coords[1]][coords[0]] = game_object

    def remove_game_object(self, game_object: GameObject) -> None:
        coords = game_object.get_coords()

        self._map[coords[1]][coords[0]] = None

        self._removed.append(game_object)

    def move_game_object(
        self, last_coords: tuple[int, int], new_coords: tuple[int, int]
    ) -> None:
        obj = self._map[last_coords[1]][last_coords[0]]
        self._map[last_coords[1]][last_coords[0]] = None
        self._map[new_coords[1]][new_coords[0]] = obj

    def is_cell_empty(self, coords: tuple[int, int]) -> bool:
        if _is_in_bound(coords[0], self.get_width()) and _is_in_bound(
            coords[1], self.get_height()
        ):
            return not bool(self._map[coords[1]][coords[0]])

        return False

    def get_max_agents_level(self) -> int:
        max_level = 0

        for row in self._map:
            for obj in row:
                if isinstance(obj, Agent):
                    level = obj.get_level()

                    if level > max_level:
                        max_level = level

        return max_level

    def get_agents_count(self) -> int:
        agents_count = 0

        for row in self._map:
            for obj in row:
                if isinstance(obj, Agent):
                    agents_count += 1

        return agents_count

    def get_random_empty_cell(self) -> tuple[int, int] | None:
        return self._random_cell_picker.get_random_cell()

    def is_agent_near(self, coords: tuple[int, int]) -> bool:
        objects = self._get_objects_in_square(coords)

        for obj in objects:
            if isinstance(obj, Agent):
                return True

        return False

    def get_agent_in_coords(self, coords: tuple[int, int]) -> GameObject | None:
        if _is_in_bound(coords[0], self.get_width()) and _is_in_bound(
            coords[1], self.get_height()
        ):
            obj = self._map[coords[1]][coords[0]]

            return obj if isinstance(obj, Agent) else None

        return None

    def get_nearest_food_coords_by_radius(
        self, coords_from: tuple[int, int], radius: int
    ) -> tuple[int, int] | None:
        for r in range(1, radius + 1):
            objects = self._get_objects_in_square(coords_from, r)

            for obj in objects:
                if isinstance(obj, Food):
                    return obj.get_coords()
        return None

    def is_food_near_coords(self, coords: tuple[int, int]) -> bool:
        food_coords = self.get_nearest_food_coords_by_radius(coords, 1)

        return bool(food_coords)

    def update(self) -> None:
        self._ticks += 1

        to_update = []

        for row in self._map:
            for obj in row:
                if obj:
                    to_update.append(obj)

        for obj in to_update:
            if obj not in self._removed:
                obj.update()

        self._removed.clear()

        for factory in self._factories:
            factory.update()

    def _get_objects_in_square(
        self, coords: tuple[int, int], radius: int = 1
    ) -> list[GameObject]:
        """
        if radius == 1
        [
            [x, x, x],
            [x, o, x],
            [x, x, x],
        ]

        if radius == 2
        [
            [x, x, x, x, x]
            [x, o, o, o, x]
            [x, o, o, o, x]
            [x, o, o, o, x]
            [x, x, x, x, x]
        ]

        etc...

        return all objects marked like "x" in upper diagram
        """

        square_coords = self.get_square_coords(coords, radius)
        square_coords = list(
            filter(
                lambda c: _is_in_bound(c[0], self._field_width)
                and _is_in_bound(c[1], self._field_height),
                square_coords,
            )
        )

        # print(square_coords)

        objects = [self._map[c[1]][c[0]] for c in square_coords]

        return objects

    def get_square_coords(
        self, middle_coords: tuple[int, int], radius: int = 1
    ) -> list[tuple[int, int]]:
        perms = product(range(-radius, radius + 1), repeat=2)
        coords = [
            (middle_coords[0] + perm[0], middle_coords[1] + perm[1]) for perm in perms
        ]

        current_radius = radius - 1
        while current_radius >= 0:
            excluded_perms = product(
                range(-current_radius, current_radius + 1), repeat=2
            )
            excluded_coords = [
                (middle_coords[0] + perm[0], middle_coords[1] + perm[1])
                for perm in excluded_perms
            ]

            # print(excluded_coords)
            coords = [v for v in coords if v not in excluded_coords]

            current_radius -= 1

        return coords


class RandomCellPicker:
    def __init__(self, scene: Scene) -> None:
        self._scene = scene

    def get_random_cell(self) -> tuple[int, int] | None:
        scene_map = self._scene.get_map()

        empty_cells_coords: list[tuple[int, int]] = []

        for y, row in enumerate(scene_map):
            for x, game_object in enumerate(row):
                if not game_object:
                    empty_cells_coords.append((x, y))

        return choice(empty_cells_coords) if empty_cells_coords else None
