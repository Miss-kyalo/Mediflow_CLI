import json
from pathlib import Path


class StorageManager:
    def __init__(self, file_path: str | Path = "data/clinic_data.json"):
        self.file_path = Path(file_path)

    def load_data(self) -> dict:
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            return {}

        with self.file_path.open("r", encoding="utf-8") as data_file:
            data = json.load(data_file)

        if not isinstance(data, dict):
            raise ValueError("Storage data must contain a JSON object")
        return data

    def save_data(self, data: dict) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.file_path.with_suffix(self.file_path.suffix + ".tmp")
        with temporary_path.open("w", encoding="utf-8") as data_file:
            json.dump(data, data_file, indent=2)
        temporary_path.replace(self.file_path)
