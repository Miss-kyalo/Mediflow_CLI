from __future__ import annotations
import json
import logging
import shutil
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


class StorageManager:

    def __init__(self, file_path: str | Path = "data/clinic_data.json"):
        self.file_path = Path(file_path)
        self.backup_path = self.file_path.with_suffix(self.file_path.suffix + ".bak")
        self.temp_path = self.file_path.with_suffix(self.file_path.suffix + ".tmp")

    def create_backup(self) -> bool:
        if not self.file_path.exists():
            return False
        try:
            shutil.copy2(self.file_path, self.backup_path)
            logger.info(f"Backup created successfully at {self.backup_path}")
            return True
        except OSError as error:
            logger.error(f"Failed to create backup for {self.file_path}: {error}")
            return False

    def load_data(self) -> Dict[str, Any]:
        data = self._read_file(self.file_path)

        if data is None and self.backup_path.exists():
            logger.warning(
                f"Primary file {self.file_path} invalid or missing. Restoring from backup..."
            )
            data = self._read_file(self.backup_path)
            if data is not None:
                logger.info("Successfully recovered data from backup.")
                self.save_data(data)

        return data if data is not None else {}

    def _read_file(self, target_path: Path) -> Dict[str, Any] | None:
        if not target_path.exists() or target_path.stat().st_size == 0:
            return None

        try:
            with target_path.open("r", encoding="utf-8") as data_file:
                data = json.load(data_file)
            if not isinstance(data, dict):
                logger.error(f"Data in {target_path} must be a JSON object (dict).")
                return None
            return data
        except (json.JSONDecodeError, OSError) as error:
            logger.error(f"Error reading {target_path}: {error}")
            return None

    def save_data(self, data: Dict[str, Any]) -> bool:
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            if self.file_path.exists():
                self.create_backup()

            with self.temp_path.open("w", encoding="utf-8") as data_file:
                json.dump(data, data_file, indent=2, default=str)

            self.temp_path.replace(self.file_path)
            return True

        except (OSError, TypeError) as error:
            logger.error(f"Error saving data to {self.file_path}: {error}")
            return False
        finally:
            if self.temp_path.exists():
                try:
                    self.temp_path.unlink()
                except OSError:
                    pass