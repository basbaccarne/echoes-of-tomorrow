import os
import yaml


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")


def _load_config(path: str = CONFIG_PATH) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


_config = _load_config()

SERVER_IP       = _config.get("serverip",       "127.0.0.1")
AUDIO_CARD      = _config.get("audio_card",      "default")
AUDIO_CARD_RING = _config.get("audio_card_ring", "i2s_amp")
AUDIO_VOLUME    = _config.get("audio_volume",    80)
UNIQUE_PORTS    = _config.get("unique_port",     {})


class SharedState:
    booth_id = 0