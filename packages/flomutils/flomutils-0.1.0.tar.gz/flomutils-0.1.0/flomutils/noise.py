import random

def add_noise(motion, randomness):
    for t, frame in motion.keyframes():
        new_frame = frame.get()
        positions = {
            k: v + random.random() * randomness
            for k, v in new_frame.positions.items()
        }
        new_frame.positions = positions
        frame.set(new_frame)
