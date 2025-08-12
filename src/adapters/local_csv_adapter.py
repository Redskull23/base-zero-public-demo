import csv
from typing import Iterator, Dict, Any, List

class LocalCSVAdapter:
    """Reads CSVs from examples/synthetic_tables and yields rows with table_name."""
    def __init__(self, table_paths: List[str]):
        self.table_paths = table_paths

    def rows(self) -> Iterator[Dict[str, Any]]:
        for path in self.table_paths:
            table_name = path.split("/")[-1].replace(".csv", "")
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    r["__table__"] = table_name
                    yield r
