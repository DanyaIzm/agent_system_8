import csv
import os
from data_dumper import DataDumpInfo, DataDumper
import dataclasses


class CSVDumper(DataDumper):
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

        os.remove(file_path)

        self._csvfile = open(self._file_path, "w+", newline="")
        self._csvwriter = csv.DictWriter(
            self._csvfile, fieldnames=[f.name for f in dataclasses.fields(DataDumpInfo)]
        )
        self._csvwriter.writeheader()

    def dump(self, data: DataDumpInfo) -> None:
        print([data.eaten_agents, data.spawned_agents])
        self._csvwriter.writerow(dataclasses.asdict(data))

    def close(self) -> None:
        self._csvfile.close()
