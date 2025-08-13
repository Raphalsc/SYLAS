import json
import time
import os

from .sensor_ppg import read_ppg
from .sensor_temp import read_temp
from .sensor_gsr import read_gsr
from .sensor_imu import read_imu
from .sensor_audio import read_audio

PERCEPTION_STATE_FILE = "memory_data/perception_state.json"
OVERRIDES_FILE = "memory_data/sensor_overrides.json"

def load_overrides():
    """Charge les valeurs forcées si elles existent"""
    if os.path.exists(OVERRIDES_FILE) and os.path.getsize(OVERRIDES_FILE) > 0:
        try:
            with open(OVERRIDES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def apply_overrides(state, overrides):
    """Applique les valeurs forcées au state"""
    for key, value in overrides.items():
        if isinstance(value, dict) and key in state:
            state[key].update(value)
        else:
            state[key] = value
    return state

def update_perception_state():
    """Lit tous les capteurs et met à jour perception_state.json"""
    # Lecture capteurs
    state = {
        "ppg": read_ppg(),
        "temperature": read_temp(),
        "gsr": read_gsr(),
        "imu": read_imu(),
        "audio": read_audio(),
        "timestamp": time.time()
    }

    # Application des valeurs forcées
    overrides = load_overrides()
    state = apply_overrides(state, overrides)

    # Sauvegarde
    with open(PERCEPTION_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    return state

if __name__ == "__main__":
    print("Démarrage du gestionnaire de perception (simulation + overrides)")
    while True:
        data = update_perception_state()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        time.sleep(2)
