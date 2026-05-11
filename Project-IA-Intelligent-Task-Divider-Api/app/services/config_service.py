import os
import json
from typing import Dict, Any

class ConfigService:
    def __init__(self):
        self.config_path = os.getenv("CONFIG_PATH", "./data/config.json")

    def get_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            return {}
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def update_config(self, partial_data: dict) -> Dict[str, Any]:
        config = self.get_config()
        for k, v in partial_data.items():
            if v is not None:
                config[k] = v
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return config

config_service = ConfigService()
