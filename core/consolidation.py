# consolidation.py
from memory import SylasMemory
from datetime import datetime, timedelta
import numpy as np

class SylasConsolidation:
    def __init__(self, memory: SylasMemory):
        self.memory = memory

    def consolidate(self):
        now = datetime.now()
        cutoff = now - timedelta(hours=self.memory.short_term_duration_hours)

        for entry in self.memory.short_term:
            ts = datetime.fromisoformat(entry["timestamp"])
            if ts >= cutoff:
                # Ici, on peut ajouter un filtre sur importance ou émotions
                self.memory.add_long_term(
                    content=entry["content"],
                    mtype=entry["type"],
                    importance=entry["importance"],
                    emotions=entry["emotions"]
                )

        self.memory.short_term = []

