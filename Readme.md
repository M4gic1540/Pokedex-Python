# Pokémon Viewer


🎮 # Visión General
Pokémon Viewer es una aplicación de escritorio que te permite explorar el mundo Pokémon de manera interactiva. Desarrollada en Python con Tkinter, ofrece una interfaz intuitiva para acceder a información detallada de tus Pokémon favoritos, incluyendo sus evoluciones, estadísticas y movimientos.

✨ # Características Destacadas
🔍 Búsqueda Avanzada
Búsqueda por nombre con autocompletado

Historial de búsquedas recientes

Corrección ortográfica automática

🖼️ Visualización Completa
Modo Normal/Shiny: Alterna entre versiones con un clic

Imágenes HD: Sprites en alta resolución (300x300px)

Detalles completos:

Estadísticas base (HP, Ataque, Defensa, etc.)

Gráficos de radar para comparar atributos

Lista de movimientos aprendibles

🌱 Sistema de Evoluciones
Línea evolutiva completa: Visualiza todas las etapas

Detalles de evolución: Nivel, objeto o condición requerida

Carga inteligente: Solo carga evoluciones cuando se solicitan

⚡ Optimizaciones
Caché local: Reduce llamadas a la API

Spinner de carga: Feedback visual durante operaciones

Diseño responsivo: Se adapta a diferentes tamaños de pantalla

🛠️ Instalación Paso a Paso
Requisitos Previos
Python 3.8+

pip (Gestor de paquetes)

Método 1: Instalación Directa
bash

# Clonar repositorio

git clone https://github.com/tu_usuario/pokemon-viewer.git
cd pokemon-viewer

# Instalar dependencias

pip install requests Pillow
Método 2: Usando Entorno Virtual (Recomendado)
bash

# Crear y activar entorno virtual

python -m venv venv
source venv/bin/activate # Linux/macOS
.\venv\Scripts\activate # Windows

# Instalar dependencias

pip install -r requirements.txt
Archivo requirements.txt
text
requests==2.31.0
Pillow==10.0.0
🚀 Cómo Usar la Aplicación
Iniciar la aplicación:

bash
python main.py
Interfaz principal:

Barra de búsqueda superior

Grid de Pokémon aleatorios

Panel de detalles expandible

Funciones clave:

Click en cualquier Pokémon para ver detalles

Checkbox "Shiny" para alternar versiones

Scroll horizontal para evoluciones largas

🏗️ Estructura del Proyecto
text
pokemon-viewer/
├── docs/ # Documentación adicional
├── images/ # Assets gráficos
├── src/
│ ├── controllers/ # Lógica de control
│ ├── models/ # Manejo de datos
│ ├── views/ # Interfaces de usuario
│ └── utils/ # Utilidades comunes
├── main.py # Punto de entrada
├── README.md # Este archivo
└── requirements.txt # Dependencias
🤝 Contribución
¡Tu ayuda es bienvenida! Para contribuir:

Haz fork del proyecto

Crea una rama (git checkout -b feature/nueva-funcion)

Haz commit de tus cambios (git commit -am 'Agrega nueva función')

Haz push a la rama (git push origin feature/nueva-funcion)

Abre un Pull Request

📜 Licencia
Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

✉️ Contacto
Para preguntas o sugerencias:

Email: tgonzalezb24@gmail.com
