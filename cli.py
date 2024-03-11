import os
import time

from abstract_scene import AbstractScene
from agent import Agent
from food import Food
from graphical_client import GraphicalClient


class CliAgentGame(GraphicalClient):
    """Console line graphical client"""

    def __init__(self, scene: AbstractScene = None) -> None:
        super().__init__(scene)

    def update(self) -> None:
        os.system("cls")

        scene_map = self._scene.get_map()
        agents_count = 0

        agents = []

        for row in scene_map:
            print("[", end="")

            for obj in row:
                if isinstance(obj, Food):
                    print(f"f{obj.get_level()}", end="")
                elif isinstance(obj, Agent):
                    print(f"A{obj.get_level()}", end="")
                    agents_count += 1
                    agents.append(obj)
                else:
                    print("  ", end="")

            print("]\n", end="")

        most_experienced_agent = (
            max(agents, key=lambda a: a.get_level()) if agents else None
        )
        max_agents_level = (
            str(most_experienced_agent.get_level())
            if most_experienced_agent
            else "NO ALIVE"
        )

        print(f"Ticks past: {self._scene.get_ticks()}")
        print(f"Agents left: {agents_count}")
        print(f"Agents ate count: {self._scene.get_agents_ate_count()}")
        print(f"Agents spawned from other: {self._scene.get_spawned_from()}")
        print(f"Max agent's level: {max_agents_level}")

    def delay(self) -> None:
        time.sleep(0.8)
