import pygame
from abstract_scene import AbstractScene
from agent import Agent
from food import Food
from graphical_client import GraphicalClient
from functools import cache


class PygameClient(GraphicalClient):
    def __init__(self, scene: AbstractScene = None) -> None:
        super().__init__(scene)
        self._screen = pygame.display.set_mode([1200, 800])
        self._scene_surface = pygame.Surface((750, 750))
        self._clock = pygame.time.Clock()
        self._fps = 10

        pygame.font.init()

    @property
    def fps(self) -> int:
        return self._fps

    @fps.setter
    def fps(self, value: int) -> None:
        if value <= 0:
            self._fps = 2
        else:
            self._fps = value

    def update(self) -> None:
        super().update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise NotImplementedError("[DEV] Add here another exception!")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.fps -= 2
                if event.key == pygame.K_UP:
                    self.fps += 2

        self._clear_screen()
        self._clear_grid()

        self._draw_grid()
        self._draw_scene()
        self._draw_gui()

        self._screen.blit(
            self._scene_surface,
            (
                30,
                30,
            ),
        )

        pygame.display.update()

    def delay(self) -> None:
        self._clock.tick(self.fps)

    @cache
    def _get_game_object_font(self) -> pygame.font.Font:
        width, height = self._get_grid_dims()

        return pygame.font.Font("assets/SpaceMono-Bold.ttf", min(width, height) - 6)

    @cache
    def _get_gui_font(self) -> pygame.font.Font:
        return pygame.font.Font("assets/SpaceMono-Bold.ttf", 22)

    def _clear_screen(self):
        self._screen.fill((0, 0, 0))

    def _clear_grid(self) -> None:
        self._scene_surface.fill((0, 0, 0))

    def _get_grid_dims(self) -> tuple[int, int]:
        block_width = self._scene_surface.get_width() // self._scene.get_width()
        block_height = self._scene_surface.get_height() // self._scene.get_height()

        return block_width, block_height

    def _draw_grid(self) -> None:
        block_width, block_height = self._get_grid_dims()

        for x in range(0, self._scene.get_width() * block_width, block_width):
            for y in range(0, self._scene.get_height() * block_height, block_height):
                rect = pygame.Rect(x, y, block_width, block_height)
                pygame.draw.rect(self._scene_surface, (255, 255, 255), rect, 1)

    def _draw_scene(self) -> None:
        scene_map = self._scene.get_map()
        agents_count = 0

        agents = []

        grid_cell_width, grid_cell_height = self._get_grid_dims()

        circle_radius = min(grid_cell_width, grid_cell_height) // 2 - 3

        for y, row in enumerate(scene_map):
            for x, obj in enumerate(row):
                if not obj:
                    continue

                obj_cell_center_coords = (
                    x * grid_cell_width + grid_cell_width // 2,
                    y * grid_cell_height + grid_cell_height // 2,
                )

                if isinstance(obj, Food):
                    obj_circle = pygame.draw.circle(
                        self._scene_surface,
                        (82, 190, 79),
                        obj_cell_center_coords,
                        circle_radius,
                    )
                elif isinstance(obj, Agent):
                    obj_circle = pygame.draw.circle(
                        self._scene_surface,
                        (255, 0, 0),
                        obj_cell_center_coords,
                        circle_radius,
                    )
                    agents_count += 1
                    agents.append(obj)

                font = self._get_game_object_font()
                rendered_font = font.render(str(obj.get_level()), 0, (255, 255, 255))
                self._scene_surface.blit(
                    rendered_font,
                    (
                        obj_circle.topleft[0] + circle_radius // 2,
                        obj_circle.topleft[1] - circle_radius // 2,
                    ),
                )

        most_experienced_agent = (
            max(agents, key=lambda a: a.get_level()) if agents else None
        )
        max_agents_level = (
            str(most_experienced_agent.get_level())
            if most_experienced_agent
            else "NO ALIVE"
        )

    def _draw_gui(self) -> None:
        font = self._get_gui_font()

        ticks_past_font = font.render(
            f"Ticks past: {self._scene.get_ticks()}", 0, (255, 255, 255)
        )
        self._screen.blit(
            ticks_past_font,
            (
                self._scene_surface.get_width() + 30 + 10,
                30,
            ),
        )

        agents_count = self._scene.get_agents_count()
        agent_left_font = font.render(
            f"Agents left: {agents_count}", 0, (255, 255, 255)
        )
        self._screen.blit(
            agent_left_font,
            (
                self._scene_surface.get_width() + 30 + 10,
                font.get_height() * 1 + 30,
            ),
        )

        agents_ate_count_font = font.render(
            f"Agents ate count: {self._scene.get_agents_ate_count()}",
            0,
            (255, 255, 255),
        )
        self._screen.blit(
            agents_ate_count_font,
            (
                self._scene_surface.get_width() + 30 + 10,
                font.get_height() * 2 + 30,
            ),
        )

        agents_spawned_from_count_font = font.render(
            f"Agents spawned: {self._scene.get_spawned_from()}",
            0,
            (255, 255, 255),
        )
        self._screen.blit(
            agents_spawned_from_count_font,
            (
                self._scene_surface.get_width() + 30 + 10,
                font.get_height() * 3 + 30,
            ),
        )

        max_agents_level = self._scene.get_max_agents_level()
        max_agents_level_str = (
            str(max_agents_level) if max_agents_level != 0 else "NO AGENTS"
        )
        max_agents_level_font = font.render(
            f"Max agent's level: {max_agents_level_str}",
            0,
            (255, 255, 255),
        )
        self._screen.blit(
            max_agents_level_font,
            (
                self._scene_surface.get_width() + 30 + 10,
                font.get_height() * 4 + 30,
            ),
        )
