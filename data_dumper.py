from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class DataDumpInfo:
    agents_left: int
    eaten_agents: int
    spawned_agents: int
    max_agents_level: int


class DataDumper(ABC):
    """
    Used to save dump of the simulation progress
    """

    @abstractmethod
    def dump(self, data: DataDumpInfo) -> None: ...

    @abstractmethod
    def close(self) -> None: ...
