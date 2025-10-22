# bots/ping_bot.py
import random
import numpy as np

class Bot:
    def __init__(self, robot):
        self.robot = robot
        self.nombre = "PingBot"

    def decision(self):
        """Gira lentamente y dispara de vez en cuando."""
        self.robot.angulo += 0.1
        if random.random() < 0.1:
            self.robot.arena.disparar(self.robot)

