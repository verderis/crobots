# bots/sniper_bot.py
import numpy as np

class Bot:
    def __init__(self, robot):
        self.robot = robot
        self.nombre = "SniperBot"
        self.angulo_actual = 0

    def decision(self):
        """Gira lentamente y dispara solo si ve enemigos a distancia media/larga."""
        self.angulo_actual += 0.05
        self.robot.angulo = self.angulo_actual

        enemigos = [r for r in self.robot.arena.robots if r.salud > 0 and r is not self.robot]
        if enemigos:
            dx = np.array([e.x - self.robot.x for e in enemigos])
            dy = np.array([e.y - self.robot.y for e in enemigos])
            distancias = np.hypot(dx, dy)
            objetivo = np.argmin(distancias)
            if 100 < distancias[objetivo] < 400:
                self.robot.arena.disparar(self.robot)

