Mini-Crobots 🛡️

Mini-Crobots es un proyecto educativo en Python inspirado en el clásico juego Crobots.
Permite programar robots autónomos que se enfrentan en una arena con obstáculos, proyectiles y estrategias personalizadas.

✅ Aprende programación, lógica y algoritmos de manera divertida.
🎯 Visualiza los combates con GIFs animados y prueba tus propios bots.

🎬 Cómo se ve


Mini-Crobots en acción: los robots navegan, esquivan obstáculos y disparan proyectiles.

🚀 Características

Arena de combate rectangular con robots autónomos.

Obstáculos que bloquean robots y proyectiles.

Bots personalizables cargados automáticamente desde la carpeta bots/.

Movimiento, disparos y colisiones simples.

Generación automática de GIFs animados de los combates.

🗂️ Estructura del proyecto
mini-crobots/
│
├─ bots/                 # Carpeta para tus bots
│   ├─ ping_bot.py
│   ├─ seeker_bot.py
│   ├─ berserker_bot.py
│   └─ sniper_bot.py
│
├─ main.py               # Motor de simulación
└─ README.md             # Información del proyecto

⚡ Instalación rápida

Clonar el repositorio:

git clone https://github.com/usuario/mini-crobots.git
cd mini-crobots


Instalar dependencias:

pip install numpy matplotlib pillow

🏁 Cómo ejecutar

Desde Python o JupyterLab:

from main import ejecutar_combate

ganador, gif = ejecutar_combate()
print("Ganador:", ganador)


En JupyterLab, para mostrar el GIF:

from IPython.display import Image
Image(filename=gif)

🤖 Crear tu propio bot

Crear un archivo mi_bot.py dentro de bots/.

Definir la clase Bot:

class Bot:
    def __init__(self, robot):
        self.robot = robot
        self.nombre = "MiBot"

    def decision(self):
        # Cambiar ángulo
        self.robot.angulo = ...
        # Disparar proyectiles
        self.robot.arena.disparar(self.robot)


Tu bot se cargará automáticamente al ejecutar la simulación.

📚 Aprendizaje

Programación orientada a objetos en Python.

Lógica de toma de decisiones y estrategias.

Uso de numpy y matplotlib para simulación.

Manejo de colisiones y físicas simples.

Generación de animaciones y visualización de datos.

📝 Licencia

Este proyecto es open-source (MIT) y puede usarse con fines educativos.
