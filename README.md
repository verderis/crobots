🛡️ Mini-Crobots en Python

Mini-Crobots es un proyecto educativo en Python inspirado en el clásico juego Crobots, donde pequeños robots programables se enfrentan en una arena. El objetivo del proyecto es enseñar conceptos de programación, lógica y algoritmos de manera divertida, a través de la creación de bots autónomos que se mueven y disparan en una simulación.

🎯 Objetivos

Crear un entorno de simulación simple para robots autónomos.

Enseñar a programar estrategias usando Python.

Permitir la incorporación de bots personalizados cargados automáticamente desde la carpeta bots/.

Visualizar los combates mediante un GIF animado, apto para JupyterLab.

Introducir conceptos de sensores, obstáculos y colisiones de manera didáctica.

⚙️ Características

Arena de combate rectangular con dimensiones configurables.

Robots con nombre, salud, ángulo de movimiento y disparos.

Proyectiles que interactúan con robots y obstáculos.

Obstáculos aleatorios que bloquean robots y proyectiles.

Bots independientes con comportamiento programable en Python (decision()).

Generación automática de GIFs animados del combate.

Diseño modular y sencillo para estudiantes.

🗂️ Estructura del proyecto
mini-crobots/
│
├─ bots/                 # Carpeta donde se crean los bots
│   ├─ ping_bot.py
│   ├─ seeker_bot.py
│   ├─ berserker_bot.py
│   └─ sniper_bot.py
│
├─ main.py               # Motor de la arena y simulación
└─ README.md             # Información del proyecto

🚀 Cómo ejecutar

Clonar el repositorio:

git clone https://github.com/usuario/mini-crobots.git
cd mini-crobots


Instalar dependencias:

pip install numpy matplotlib pillow


Ejecutar la simulación desde Python o JupyterLab:

from main import ejecutar_combate

ganador, gif = ejecutar_combate()
print("Ganador:", ganador)


Visualizar el GIF en JupyterLab:

from IPython.display import Image
Image(filename=gif)

🛠️ Cómo crear tu propio bot

Crear un archivo mi_bot.py dentro de la carpeta bots/.

Definir la clase Bot con el constructor __init__(self, robot) y el método decision(self).

El método decision() puede modificar:

self.robot.angulo → dirección de movimiento

self.robot.arena.disparar(self.robot) → disparar proyectiles

Al ejecutar ejecutar_combate(), tu bot será cargado automáticamente.

📚 Aprendizaje

Este proyecto permite a estudiantes aprender:

Programación orientada a objetos en Python.

Lógica de toma de decisiones y estrategia.

Uso de librerías científicas (numpy, matplotlib) para simulación.

Manejo de colisiones y físicas simples.

Generación de animaciones y visualización de datos.

🔖 Licencia

Este proyecto es open-source. Puedes usarlo y modificarlo con fines educativos.
