from csv_dumper import CSVDumper
from data_dumper import DataDumper
from game import Game
from pygame_client import PygameClient


class DumperMock(DataDumper):
    def dump(self) -> None:
        pass


def main() -> None:
    graphical = PygameClient()

    # graphical = CliAgentGame()
    # dumper = DumperMock()
    dumper = CSVDumper("stat.csv")

    game = Game(graphical, dumper)

    game.run()


if __name__ == "__main__":
    main()
