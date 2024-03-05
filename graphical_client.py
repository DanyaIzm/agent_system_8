from abc import ABC, abstractmethod

from abstract_scene import AbstractScene


class NoSceneProvidedException(Exception): ...


class GraphicalClient(ABC):
    """
    Renders scene
    """

    def __init__(self, scene: AbstractScene = None) -> None:
        self._scene = scene

    def set_scene(self, scene: AbstractScene) -> None:
        self._scene = scene

    @abstractmethod
    def update(self) -> None:
        """
        Updates graphical client into one tick.

        MUST be overridden by subclasses

        Raises:
            NoSceneProvidedException: scene shoud be set by contructor or set_scene method
        """
        if not self._scene:
            raise NoSceneProvidedException("Scene was not provided to graphical client")

    @abstractmethod
    def delay(self) -> None:
        """
        Make a delay in program execution on order to update screen not too fast
        """
        ...
