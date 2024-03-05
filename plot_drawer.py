import csv
import os
from dataclasses import fields
from typing import Any

import matplotlib.pyplot as plt

from data_dumper import DataDumpInfo


class OSEntityExistsException(Exception): ...


def _get_nearest_square(limit: int):
    result = 0

    while (result + 1) ** 2 <= limit:
        result += 1

    return result


def _convert_from_snake_to_normal(string: str) -> str:
    return " ".join([s.title() for s in string.split("_")])


def _flatten(_list: list[list[Any]]) -> list[Any]:
    flat_list = []

    for row in _list:
        flat_list.extend(row)

    return flat_list


class CSVPlotDrawer:
    def __init__(self, file_path: str, plot_directory: str) -> None:
        self._file_path = file_path
        self._plot_directory = plot_directory

    def draw(self) -> None:
        data = self._read_data_from_csv()

        self._ensure_directory_exists()

        for k, v in data.items():
            plt.clf()
            plt.plot(v)
            plt.title(_convert_from_snake_to_normal(k))
            plt.savefig(os.path.join(self._plot_directory, k + ".png"))

        # print combined plot
        subplot_height = _get_nearest_square(len(data.keys()))

        fig, axes = plt.subplots(subplot_height, subplot_height)

        subplots = _flatten(axes)

        for index, (k, v) in enumerate(data.items()):
            subplots[index].plot(v)
            subplots[index].set_title(_convert_from_snake_to_normal(k))

        fig.tight_layout()
        plt.savefig(os.path.join(self._plot_directory, "combined.png"))

    def _read_data_from_csv(self) -> dict[str, Any]:
        with open(self._file_path, "r") as csv_file:
            reader = csv.DictReader(
                csv_file, fieldnames=[f.name for f in fields(DataDumpInfo)]
            )

            full_data = {}

            for data in reader:
                for k, v in data.items():
                    if k == v:
                        continue
                    if not full_data.get(k):
                        full_data[k] = [int(v)]
                    else:
                        full_data[k].append(int(v))

        return full_data

    def _ensure_directory_exists(self) -> None:
        if os.path.exists(self._plot_directory):
            if not os.path.isdir(self._plot_directory):
                raise OSEntityExistsException(
                    f"OS entity {self._plot_directory} is not a directory"
                )

            return

        os.mkdir(self._plot_directory)


if __name__ == "__main__":
    CSVPlotDrawer("stat.csv", "plots").draw()
