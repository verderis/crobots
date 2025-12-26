# bots/berserker_bot.py
import numpy as np

class Bot:
    def __init__(self, robot):
        self.robot = robot
        self.nombre = "BerserkerBot"
        self.tiempo = 0

    def decision(self):
        """Gira oscilando y dispara siempre."""
        self.tiempo += 1
        self.robot.angulo += np.sin(self.tiempo * 0.1) * 0.2
        self.robot.arena.disparar(self.robot)


