import random

def read_temp():
    """Température cutanée en °C (simulation haute précision)"""
    return round(random.uniform(33.0, 36.5), 2)
