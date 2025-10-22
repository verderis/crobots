import numpy as np
import random

class Bot:
    def __init__(self, robot):
        self.robot = robot

    def decision(self):
        """Gira lentamente y dispara de vez en cuando."""
        self.robot.angulo += 0.1
        if random.random() < 0.1:
            self.robot.arena.disparar(self.robot)