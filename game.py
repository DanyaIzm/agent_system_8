from typing import NoReturn

from agent import AgentFactory
from data_dumper import DataDumper, DataDumpInfo
from food import FoodFactory
from graphical_client import GraphicalClient
from scene import Scene


class Game:
    def __init__(
        self,
        graphical_client: GraphicalClient,
        datadumper: DataDumper,
    ) -> None:
        self._datadumper = datadumper
        self._graphical_client = graphical_client
        self._scene = None

    def run(self) -> NoReturn:
        """Run the simulation"""

        self._scene = Scene()

        self._graphical_client.set_scene(self._scene)

        agent_factory = AgentFactory(self._scene)
        food_factory = FoodFactory(self._scene)

        agent_factory.spawn_radom(10)
        food_factory.spawn_bunch(16)

        self._loop()

    def _loop(self) -> NoReturn:
        while True:
            self._graphical_client.update()

            self._datadumper.dump(
                data=DataDumpInfo(
                    self._scene.get_agents_count(),
                    self._scene.get_agents_ate_count(),
                    self._scene.get_spawned_from(),
                    self._scene.get_max_agents_level(),
                )
            )

            self._scene.update()

            self._graphical_client.delay()
