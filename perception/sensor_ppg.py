import random
import time

def read_ppg():
    """Simule un capteur PPG : BPM, HRV, SpO2"""
    bpm = random.randint(55, 90)  # battements par minute
    hrv = round(random.uniform(20, 80), 1)  # ms
    spo2 = round(random.uniform(95, 100), 1)  # %
    return {
        "bpm": bpm,
        "hrv": hrv,
        "spo2": spo2
    }
