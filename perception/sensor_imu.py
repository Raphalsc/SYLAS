import random

def read_imu():
    """Simule un BMI270 (accéléromètre + gyroscope)"""
    accel = {
        "x": round(random.uniform(-2, 2), 3),
        "y": round(random.uniform(-2, 2), 3),
        "z": round(random.uniform(-2, 2), 3)
    }
    gyro = {
        "x": round(random.uniform(-250, 250), 3),
        "y": round(random.uniform(-250, 250), 3),
        "z": round(random.uniform(-250, 250), 3)
    }
    return {"accel": accel, "gyro": gyro}
