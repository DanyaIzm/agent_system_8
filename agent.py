from abc import ABC, abstractmethod
from copy import deepcopy
from random import randint, choice
from math import copysign
import time
from abstract_scene import AbstractScene

from game_object import GameObject


# oxo
# xox
# oxo
_WALKING_VECTORS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class UnableToSpawnException(Exception): ...


class AgentFactory:
    def __init__(self, scene: AbstractScene) -> None:
        self._scene = scene

        scene.add_factory(self)

    def spawn_radom(self, amount: int) -> None:
        for _ in range(amount):
            coords = self._scene.get_random_empty_cell()
            self.spawn(coords)

    def spawn(self, coords: tuple[int, int], agent=None):
        if not agent:
            agent = Agent(coords, self._scene, self)

        self._scene.add_game_object(agent, coords)

    def spawn_from(self, agent):
        self._scene.increment_spawned_from()

        square_coords = self._scene.get_square_coords(agent._coords)

        square_coords = list(
            filter(lambda c: self._scene.is_cell_empty(c), square_coords)
        )

        if not square_coords:
            raise UnableToSpawnException(f"Can't spawn agent near {agent.get_coords()}")

        random_coords = choice(square_coords)

        new_agent = Agent(random_coords, agent._scene, self, level=agent._level)
        new_agent._saturation = agent._saturation // 2
        new_agent._experience = agent._experience

        self.spawn(random_coords, new_agent)

    def update(self) -> None:
        pass


class Agent(GameObject):
    def __init__(
        self,
        coords: tuple[int, int],
        scene,
        agent_factory: AgentFactory,
        level: int = 1,
    ) -> None:
        super().__init__(coords)
        self._level = level
        self._saturation = self.get_max_saturation() * 0.8
        self._scene = scene
        self._agent_factory = agent_factory
        self._experience = 0
        self._random_walk_vector = None

        self.update_state()

    def get_saturation(self) -> float:
        return self._saturation

    def get_level(self) -> int:
        return self._level

    def get_experience(self) -> int:
        return self._experience

    def get_exp_requirement(self) -> int:
        return self._level * 10

    def get_max_saturation(self) -> float:
        return self.get_exp_requirement()

    def get_fov(self) -> int:
        return 3 + self._level

    def get_waitng_hunger(self) -> float:
        return self.get_exhaustion() / 4

    def get_exhaustion(self) -> float:
        return (0.12 * self._level) / 4

    def update_state(self) -> None:
        max_saturation = self.get_max_saturation()

        if max_saturation * 0.8 <= self._saturation <= max_saturation:
            self._state = AgentSaturatedState(self)
        elif max_saturation * 0.3 <= self._saturation <= max_saturation * 0.8:
            self._state = AgentHungryState(self)
        elif self._saturation > 0:
            self._state = AgentExhastedState(self)
        else:
            self._state = AgentDeadState(self)

    def _levelup(self) -> None:
        self._level += 1

    def _can_move(self, vector) -> bool:
        coords = (self._coords[0] + vector[0], self._coords[1] + vector[1])

        return self._scene.is_cell_empty(coords)

    def _walk_to(self, coords: tuple[int, int]) -> None:
        cant_move = False

        delta_x = abs(coords[0] - self._coords[0])
        delta_y = abs(coords[1] - self._coords[1])

        if delta_x > delta_y:
            vector = (int(copysign(1, coords[0] - self._coords[0])), 0)

            if self._can_move(vector):
                self._coords = (
                    self._coords[0] + vector[0],
                    self._coords[1] + vector[1],
                )
            else:
                cant_move = True
        elif delta_y >= delta_x:
            cant_move = False
            vector = (0, int(copysign(1, coords[1] - self._coords[1])))

            if self._can_move(vector):
                self._coords = (
                    self._coords[0] + vector[0],
                    self._coords[1] + vector[1],
                )
            else:
                cant_move = True

        if cant_move:
            self._walk_random()

    def _choose_radom_walk_vector(self) -> None:
        vectors = deepcopy(_WALKING_VECTORS)

        while vectors:
            vector = choice(vectors)

            self._random_walk_vector = vector

            new_coords = (
                self._coords[0] + self._random_walk_vector[0],
                self._coords[1] + self._random_walk_vector[1],
            )

            if self._scene.is_cell_empty(new_coords):
                return
            else:
                vectors.remove(vector)

        self._random_walk_vector = (0, 0)

    def _walk_random(self) -> None:
        while True:
            if not self._random_walk_vector:
                self._choose_radom_walk_vector()

            new_coords = (
                self._coords[0] + self._random_walk_vector[0],
                self._coords[1] + self._random_walk_vector[1],
            )

            if new_coords == self._coords:
                self._random_walk_vector = None
                return

            if self._scene.is_cell_empty(new_coords):
                self._coords = new_coords
                return

            self._random_walk_vector = None

    def update(self) -> None:
        last_coords = self._coords

        # try eat another agent
        if self._scene.is_agent_near(self._coords):
            # get object in walking distance
            for wv in _WALKING_VECTORS:
                coords = (
                    self._coords[0] + wv[0],
                    self._coords[1] + wv[1],
                )

                agent = self._scene.get_agent_in_coords(coords)
                if agent:
                    if agent.get_level() < self._level:
                        # eat agent if it's level is lower than current agent's level
                        self._saturation += agent.get_saturation()
                        self._coords = coords
                        self._scene.remove_game_object(agent)
                        self._scene.move_game_object(last_coords, coords)
                        self._scene.increment_agents_ate_count()
                        self._experience = agent.get_experience()
                        return

        self.update_state()
        self._state.update()

        # eating
        if self._scene.is_food_near_coords(self._coords):
            self._experience += 1
            next_saturation = self._saturation + 1

            if next_saturation < self.get_max_saturation():
                self._saturation = next_saturation
            else:
                self._saturation = self.get_max_saturation()

        # level up
        if self._experience >= self.get_exp_requirement():
            self._levelup()

        if last_coords == self._coords:
            self._saturation -= self.get_waitng_hunger()
        else:
            self._saturation -= self.get_exhaustion()
            self._scene.move_game_object(last_coords, self._coords)


class AgentState(ABC):
    def __init__(self, agent: Agent) -> None:
        self._agent = agent

    @abstractmethod
    def update(self) -> None: ...


class AgentSaturatedState(AgentState):
    def update(self) -> None:
        if self._agent._saturation >= self._agent.get_max_saturation() * 0.85:
            self._agent._agent_factory.spawn_from(self._agent)
            self._agent._saturation //= 2
        else:
            AgentHungryState(self._agent).update()


class AgentHungryState(AgentState):
    def update(self) -> None:
        coords = self._agent._scene.get_nearest_food_coords_by_radius(
            self._agent._coords, round(self._agent.get_fov())
        )

        if coords:
            self._agent._walk_to(coords)
        else:
            self._agent._walk_random()


class AgentExhastedState(AgentState):
    def update(self) -> None:
        coords = self._agent._scene.get_nearest_food_coords_by_radius(
            self._agent._coords, round(self._agent.get_fov())
        )

        if coords:
            self._agent._walk_to(coords)
        else:
            # just stay and wait
            return


class AgentDeadState(AgentState):
    def update(self) -> None:
        self._agent._scene.remove_game_object(self._agent)
