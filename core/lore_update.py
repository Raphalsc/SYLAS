# lore_update.py
import json
import os
from datetime import datetime

class LoreUpdater:
    def __init__(self, lore_file="lore.txt"):
        self.lore_file = lore_file
        if not os.path.exists(self.lore_file):
            with open(self.lore_file, "w", encoding="utf-8") as f:
                f.write("# Lore & Personnalité de SYLAS\n\n")

    def add_to_lore(self, insight):
        with open(self.lore_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {insight}\n")

    def get_lore(self):
        with open(self.lore_file, "r", encoding="utf-8") as f:
            return f.read()
