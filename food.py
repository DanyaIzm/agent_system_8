import time
from game_object import GameObject
from random import random


_FOOD_SPAWN_PROBABILITIES = {
    1: 0.4,
    2: 0.7,
    3: 0.85,
    4: 0.95,
    5: 100,
}


class FoodFactory:
    def __init__(self, scene) -> None:
        self._scene = scene

        scene.add_factory(self)

    def update(self) -> None:
        self.spawn_radom_food()

    def spawn_radom_food(self) -> None:
        random_number = random()

        for level, food_spawn_probability in _FOOD_SPAWN_PROBABILITIES.items():
            if random_number <= food_spawn_probability:
                self._spawn_food(level)
                return

    def spawn_bunch(self, amount: int = 1) -> None:
        for _ in range(amount):
            self.spawn_radom_food()

    def _spawn_food(self, level: int) -> None:
        coords = self._scene.get_random_empty_cell()
        self._scene.add_game_object(Food(coords, level, self._scene), coords)


class Food(GameObject):
    def __init__(self, coords: tuple[int, int], level: int, scene) -> None:
        super().__init__(coords)

        self._level = level
        self._scene = scene
        self._capacity = self.get_max_capacity()

    def get_level(self) -> int:
        return self._level

    def get_max_capacity(self) -> float:
        return 5 * self._level

    def get_exhaustion(self) -> float:
        return 0.1 * self._level

    def update(self) -> None:
        self._capacity -= self.get_exhaustion()

        # kill the food
        if self._capacity <= 0:
            self._scene.remove_game_object(self)
            return

        if self._scene.is_agent_near(self._coords):
            self._capacity -= 1
