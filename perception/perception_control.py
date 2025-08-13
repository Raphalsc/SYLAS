import json
import os

# chemin robuste (fichier placé dans memory_data)
STATE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "memory_data", "perception_state.json"))

DEFAULT_STATE = {
    "heart_rate": 70,
    "hrv": 50,
    "skin_temp": 33.5,
    "gsr": 0.5,
    "acceleration": [0.0, 0.0, 0.0],
    "environment_sound": "silence"
}

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # ensure keys exist
                for k, v in DEFAULT_STATE.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception:
            # si corrompu, on réinitialise
            print("[WARN] perception_state.json corrompu ou illisible, réinitialisation au défaut.")
            save_state(DEFAULT_STATE)
            return DEFAULT_STATE.copy()
    else:
        # création automatique si absent
        save_state(DEFAULT_STATE)
        return DEFAULT_STATE.copy()

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def show_state(state):
    print("\n--- État actuel des capteurs ---")
    for k, v in state.items():
        print(f"{k}: {v}")
    print("------------------------------\n")

def main():
    state = load_state()

    print("=== Contrôle en direct des capteurs SYLAS ===")
    print("Tape 'exit' pour quitter.")
    print("Format: nom_capteur nouvelle_valeur (ex: heart_rate 85)")
    print("Capteurs disponibles:", ", ".join(state.keys()))

    while True:
        show_state(state)
        cmd = input("Commande > ").strip()
        if cmd.lower() == "exit":
            save_state(state)
            print("✅ État sauvegardé, fermeture du panneau de contrôle.")
            break

        if " " not in cmd:
            print("⚠ Format : nom_capteur valeur (ex: heart_rate 75)")
            continue

        key, value = cmd.split(" ", 1)
        if key not in state:
            print("❌ Capteur inconnu.")
            continue

        # conversion simple : json/list / float / int / string
        parsed = None
        try:
            if value.startswith("[") and value.endswith("]"):
                parsed = json.loads(value)
            else:
                # try int then float else keep string
                try:
                    parsed = int(value)
                except ValueError:
                    try:
                        parsed = float(value)
                    except ValueError:
                        parsed = value
        except Exception as e:
            print("❌ erreur parsing valeur:", e)
            continue

        state[key] = parsed
        save_state(state)
        print(f"✅ {key} mis à jour -> {parsed}")

if __name__ == "__main__":
    main()
