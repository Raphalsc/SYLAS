import random

def read_audio():
    """Simulation micro : bruit ambiant et détection de mots-clés"""
    ambiances = ["silence", "conversation", "bruit de rue", "vent", "musique", "intérieur calme"]
    ambiance = random.choice(ambiances)
    volume_db = round(random.uniform(20, 80), 1)  # dB SPL
    detected_keywords = random.choice([[], ["bonjour"], ["aide"], ["attention"], []])
    return {
        "ambiance": ambiance,
        "volume_db": volume_db,
        "keywords": detected_keywords
    }
