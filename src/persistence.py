import json
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


class StorageManager:
    """Handles JSON file storage with atomic writes, backup generation, and error handling."""

    def __init__(self, file_path: str | Path = "data/clinic_data.json"):
        self.file_path = Path(file_path)

    def create_backup(self) -> bool:
        """Create a backup copy (.bak) of the current JSON database file."""
        if not self.file_path.exists():
            return False
        try:
            backup_path = self.file_path.with_suffix(self.file_path.suffix + ".bak")
            shutil.copy2(self.file_path, backup_path)
            logger.info(f"Backup created successfully at {backup_path}")
            return True
        except OSError as error:
            logger.error(f"Failed to create backup for {self.file_path}: {error}")
            return False

    def load_data(self) -> dict:
        """Load data from JSON file safely. Returns empty dict if missing or invalid."""
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            return {}

        try:
            with self.file_path.open("r", encoding="utf-8") as data_file:
                data = json.load(data_file)
            if not isinstance(data, dict):
                logger.error("Storage data must contain a JSON object.")
                return {}
            return data
        except (json.JSONDecodeError, OSError) as error:
            logger.error(f"Error loading data from {self.file_path}: {error}")
            return {}

    def save_data(self, data: dict) -> bool:
        """Save dictionary data to JSON file using atomic file swap with automatic backup."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create a backup of existing file before overwriting
            if self.file_path.exists():
                self.create_backup()

            temporary_path = self.file_path.with_suffix(self.file_path.suffix + ".tmp")
            with temporary_path.open("w", encoding="utf-8") as data_file:
                json.dump(data, data_file, indent=2)
            temporary_path.replace(self.file_path)
            return True
        except (OSError, TypeError) as error:
            logger.error(f"Error saving data to {self.file_path}: {error}")
            return False