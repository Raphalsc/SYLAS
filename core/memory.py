import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from datetime import datetime

MEMORY_FILE = "memory_data/memories.json"
FAISS_INDEX_FILE = "memory_data/context_index.faiss"
JOURNAL_FILE = "memory_data/journal_brut.json"
NARRATIVE_FILE = "memory_data/memoire_narrative.json"

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Charger FAISS
if os.path.exists(FAISS_INDEX_FILE) and os.path.getsize(FAISS_INDEX_FILE) > 0:
    try:
        index = faiss.read_index(FAISS_INDEX_FILE)
    except:
        index = faiss.IndexFlatL2(384)
else:
    index = faiss.IndexFlatL2(384)

# Charger mémoire FAISS
if os.path.exists(MEMORY_FILE) and os.path.getsize(MEMORY_FILE) > 0:
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memories = json.load(f)
    except json.JSONDecodeError:
        memories = []
else:
    memories = []

# Charger journal brut
if os.path.exists(JOURNAL_FILE) and os.path.getsize(JOURNAL_FILE) > 0:
    try:
        with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
            journal_brut = json.load(f)
    except json.JSONDecodeError:
        journal_brut = []
else:
    journal_brut = []

# ---- FAISS standard ----
def save_memory(text, meta=None):
    global memories, index
    if meta is None:
        meta = {}
    memory_entry = {
        "text": text,
        "meta": meta,
        "date": datetime.now().isoformat()
    }
    memories.append(memory_entry)
    vector = embedder.encode([text])
    index.add(np.array(vector, dtype="float32"))
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=2, ensure_ascii=False)
    faiss.write_index(index, FAISS_INDEX_FILE)

def recall_memories(query, top_k=50):
    if len(memories) == 0:
        return []
    if query.strip() == "":
        return [m["text"] for m in memories]
    vector = embedder.encode([query])
    D, I = index.search(np.array(vector, dtype="float32"), top_k)
    return [memories[idx]["text"] for idx in I[0] if 0 <= idx < len(memories)]

# ---- Journal brut ----
def save_journal_entry(role, text):
    global journal_brut
    journal_brut.append({
        "time": datetime.now().isoformat(),
        "role": role,
        "text": text
    })
    with open(JOURNAL_FILE, "w", encoding="utf-8") as f:
        json.dump(journal_brut, f, indent=2, ensure_ascii=False)

def load_full_journal():
    if not journal_brut:
        return ""
    return "\n".join(f"[{e['role']}] {e['text']}" for e in journal_brut)

# ---- Mémoire narrative ----
def load_narrative_memory():
    if os.path.exists(NARRATIVE_FILE):
        with open(NARRATIVE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def save_narrative_memory(text):
    with open(NARRATIVE_FILE, "w", encoding="utf-8") as f:
        f.write(text.strip())
