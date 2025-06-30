#pokemon_view.py
# Interfaz de usuario para visualizar Pokémon

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests


class PokemonView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.root.title("Pokémon Viewer")
        self.root.geometry("1280x720")

        # Configurar estilo para frames shiny
        style = ttk.Style()
        style.configure("Shiny.TFrame", background="gold", bordercolor="gold")

        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame de búsqueda
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(fill=tk.X, pady=10)

        # Entrada de búsqueda
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Botón de búsqueda
        search_btn = ttk.Button(
            search_frame, text="Buscar Pokémon", command=self.controller.search_pokemon
        )
        search_btn.pack(side=tk.LEFT, padx=5)

        # Botón para refrescar
        refresh_btn = ttk.Button(
            search_frame,
            text="Mostrar Pokémon Aleatorios",
            command=self.controller.load_random_pokemons,
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Checkbutton para shiny
        self.shiny_var = tk.BooleanVar(value=False)
        shiny_btn = ttk.Checkbutton(
            search_frame,
            text="Mostrar Shiny",
            variable=self.shiny_var,
            command=self.controller.toggle_shiny_mode,
        )
        shiny_btn.pack(side=tk.LEFT, padx=5)

        # Frame para la cuadrícula de Pokémon
        self.pokemon_frame = ttk.Frame(self.main_frame)
        self.pokemon_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para detalles
        self.detail_frame = ttk.LabelFrame(
            self.main_frame, text="Detalles del Pokémon", padding="10"
        )
        self.detail_frame.pack(fill=tk.X, pady=10)

        # Elementos de detalles
        self.detail_name = ttk.Label(
            self.detail_frame, text="", font=("Arial", 12, "bold")
        )
        self.detail_name.pack()

        self.detail_image = ttk.Label(self.detail_frame)
        self.detail_image.pack()

        self.detail_types = ttk.Label(self.detail_frame, text="")
        self.detail_types.pack()

        self.detail_stats = ttk.Label(self.detail_frame, text="")
        self.detail_stats.pack()

    def clear_pokemon_grid(self):
        """Limpia todos los widgets del frame de Pokémon"""
        for widget in self.pokemon_frame.winfo_children():
            widget.destroy()

    def create_pokemon_card(self, pokemon, idx):
        """Crea una tarjeta visual para un Pokémon"""
        # Usar estilo diferente para Pokémon shiny
        style = "Shiny.TFrame" if pokemon["shiny"] else "TFrame"
        card_frame = ttk.Frame(
            self.pokemon_frame, borderwidth=1, relief="solid", padding="5", style=style
        )
        card_frame.grid(row=idx // 5, column=idx % 5, padx=5, pady=5)

        try:
            # Cargar imagen
            response = requests.get(pokemon["image"])
            img = Image.open(BytesIO(response.content)).resize((96, 96))
            photo = ImageTk.PhotoImage(img)

            img_label = ttk.Label(card_frame, image=photo)
            img_label.image = photo
            img_label.pack()

            # Nombre e ID
            name_text = f"{pokemon['name'].capitalize()} (#{pokemon['id']})"
            if pokemon["shiny"]:
                name_text += " ✨"  # Indicador shiny
            name_label = ttk.Label(card_frame, text=name_text, font=("Arial", 10))
            name_label.pack()

            # Tipos
            types_text = ", ".join(pokemon["types"])
            types_label = ttk.Label(card_frame, text=types_text)
            types_label.pack()

            # Eventos de clic
            card_frame.bind(
                "<Button-1>",
                lambda e, p=pokemon: self.controller.show_pokemon_details(p),
            )
            img_label.bind(
                "<Button-1>",
                lambda e, p=pokemon: self.controller.show_pokemon_details(p),
            )
            name_label.bind(
                "<Button-1>",
                lambda e, p=pokemon: self.controller.show_pokemon_details(p),
            )
            types_label.bind(
                "<Button-1>",
                lambda e, p=pokemon: self.controller.show_pokemon_details(p),
            )

        except requests.exceptions.RequestException:
            error_label = ttk.Label(
                card_frame, text="Error al cargar imagen", foreground="red"
            )
            error_label.pack()

    def show_pokemon_details(self, pokemon):
        """Muestra los detalles completos del Pokémon"""
        # Limpiar frame de detalles
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        # Frame principal de detalles
        detail_main_frame = ttk.Frame(self.detail_frame)
        detail_main_frame.pack(fill=tk.BOTH, expand=True)

        # Sección izquierda (imagen grande)
        left_frame = ttk.Frame(detail_main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        try:
            response = requests.get(pokemon["image"])
            img = Image.open(BytesIO(response.content)).resize((300, 300))
            photo = ImageTk.PhotoImage(img)

            img_label = ttk.Label(left_frame, image=photo)
            img_label.image = photo
            img_label.pack()

        except requests.exceptions.RequestException:
            error_label = ttk.Label(
                left_frame, text="Error al cargar imagen", foreground="red"
            )
            error_label.pack()

        # Sección derecha (datos)
        right_frame = ttk.Frame(detail_main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Nombre y tipos
        name_frame = ttk.Frame(right_frame)
        name_frame.pack(fill=tk.X, pady=5)

        name_label = ttk.Label(
            name_frame,
            text=f"{pokemon['name'].capitalize()} (#{pokemon['id']})",
            font=("Arial", 16, "bold"),
        )
        name_label.pack(side=tk.LEFT)

        types_label = ttk.Label(
            name_frame, text=" | ".join(pokemon["types"]), font=("Arial", 12)
        )
        types_label.pack(side=tk.LEFT, padx=10)

        # Estadísticas
        stats_frame = ttk.LabelFrame(right_frame, text="Estadísticas", padding=10)
        stats_frame.pack(fill=tk.X, pady=5)

        stats_text = (
            f"Altura: {pokemon['height']/10:.1f} m\n"
            f"Peso: {pokemon['weight']/10:.1f} kg\n"
            f"HP: {pokemon['stats'].get('hp', 'N/A')}\n"
            f"Ataque: {pokemon['stats'].get('attack', 'N/A')}\n"
            f"Defensa: {pokemon['stats'].get('defense', 'N/A')}\n"
            f"Ataque Especial: {pokemon['stats'].get('special-attack', 'N/A')}\n"
            f"Defensa Especial: {pokemon['stats'].get('special-defense', 'N/A')}\n"
            f"Velocidad: {pokemon['stats'].get('speed', 'N/A')}"
        )
        stats_label = ttk.Label(stats_frame, text=stats_text, justify=tk.LEFT)
        stats_label.pack()

        # Movimientos
        moves_frame = ttk.LabelFrame(
            right_frame, text="Movimientos Principales", padding=10
        )
        moves_frame.pack(fill=tk.X, pady=5)

        moves_text = "\n".join(pokemon["moves"])
        moves_label = ttk.Label(moves_frame, text=moves_text, justify=tk.LEFT)
        moves_label.pack()

        # Evoluciones
        if len(pokemon["evolutions"]) > 1:
            evo_frame = ttk.LabelFrame(
                right_frame, text="Línea de Evolución", padding=10
            )
            evo_frame.pack(fill=tk.X, pady=5)

            evo_canvas = tk.Canvas(evo_frame, height=100)
            scroll_x = ttk.Scrollbar(
                evo_frame, orient=tk.HORIZONTAL, command=evo_canvas.xview
            )
            scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
            evo_canvas.configure(xscrollcommand=scroll_x.set)
            evo_canvas.pack(fill=tk.BOTH, expand=True)

            inner_frame = ttk.Frame(evo_canvas)
            evo_canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)

            for i, evo in enumerate(pokemon["evolutions"]):
                # Obtener imagen de la evolución
                evo_data = self.controller.model.get_pokemon_details(evo)
                if evo_data:
                    try:
                        response = requests.get(evo_data["image"])
                        img = Image.open(BytesIO(response.content)).resize((80, 80))
                        photo = ImageTk.PhotoImage(img)

                        evo_label = ttk.Label(inner_frame, image=photo)
                        evo_label.image = photo
                        evo_label.grid(row=0, column=i * 2, padx=10)

                        name_label = ttk.Label(inner_frame, text=evo.capitalize())
                        name_label.grid(row=1, column=i * 2)

                        # Dibujar flecha si no es la última evolución
                        if i < len(pokemon["evolutions"]) - 1:
                            arrow_label = ttk.Label(
                                inner_frame, text="→", font=("Arial", 20)
                            )
                            arrow_label.grid(row=0, column=i * 2 + 1, padx=5)

                    except requests.exceptions.RequestException:
                        pass

            inner_frame.update_idletasks()
            evo_canvas.config(scrollregion=evo_canvas.bbox("all"))

    def show_error(self, message):
        """Muestra un mensaje de error"""
        error_label = ttk.Label(self.pokemon_frame, text=message, foreground="red")
        error_label.grid(row=0, column=0, columnspan=5)
