# bots/seeker_bot.py
import numpy as np

class Bot:
    def __init__(self, robot):
        self.robot = robot
        self.nombre = "SeekerBot"

    def decision(self):
        """Busca el enemigo más cercano y gira hacia él."""
        enemigos = [r for r in self.robot.arena.robots if r.salud > 0 and r is not self.robot]
        if enemigos:
            # Calcula distancias y ángulo relativo
            dx = np.array([e.x - self.robot.x for e in enemigos])
            dy = np.array([e.y - self.robot.y for e in enemigos])
            distancias = np.hypot(dx, dy)
            angulos = np.arctan2(dy, dx)
            objetivo = np.argmin(distancias)
            self.robot.angulo = angulos[objetivo]
            if distancias[objetivo] < 150:
                self.robot.arena.disparar(self.robot)


