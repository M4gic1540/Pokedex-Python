from tkinter import messagebox
import random
import time
from pokemon_model import PokemonModel
from pokemon_view import PokemonView


class PokemonController:
    def __init__(self, root):
        print("[DEBUG] Inicializando controlador Pokémon")
        self.model = PokemonModel()
        self.view = PokemonView(root, self)
        self.shiny_mode = False
        self.load_random_pokemons()

    def toggle_shiny_mode(self):
        """Alterna entre modo normal y shiny"""
        self.shiny_mode = not self.shiny_mode
        print(f"[DEBUG] Modo shiny {'activado' if self.shiny_mode else 'desactivado'}")
        self.load_random_pokemons()

    def search_pokemon(self):
        """Busca un Pokémon por nombre"""
        pokemon_name = self.view.search_var.get().strip()
        if not pokemon_name:
            messagebox.showwarning("Advertencia", "Por favor ingresa un nombre de Pokémon")
            return

        print(f"[DEBUG] Buscando Pokémon: {pokemon_name} (Shiny: {self.shiny_mode})")
        start = time.time()
        pokemon = self.model.get_pokemon_details(pokemon_name, self.shiny_mode)
        duration = time.time() - start

        if pokemon is None:
            messagebox.showerror("Error", f"No se encontró el Pokémon: {pokemon_name}")
            return

        print(f"[INFO] Pokémon '{pokemon_name}' cargado en {duration:.2f} segundos")

        self.view.clear_pokemon_grid()
        self.view.create_pokemon_card(pokemon, 0)
        self.view.show_pokemon_details(pokemon)

    def load_random_pokemons(self):
        """Carga y muestra Pokémon aleatorios"""
        print("[DEBUG] Cargando Pokémon aleatorios...")
        self.view.clear_pokemon_grid()
        start = time.time()

        try:
            all_pokemons = self.model.get_pokemon_list()
            if len(all_pokemons) < 10:
                raise ValueError("No hay suficientes Pokémon para seleccionar aleatoriamente.")

            random_pokemons = random.sample(all_pokemons, 10)
            print(f"[DEBUG] Pokémon seleccionados: {random_pokemons}")

            for idx, name in enumerate(random_pokemons):
                print(f"[DEBUG] Cargando detalles de: {name}")
                pokemon = self.model.get_pokemon_details(name, self.shiny_mode)
                if pokemon:
                    self.view.create_pokemon_card(pokemon, idx)
                else:
                    print(f"[WARN] No se pudieron obtener detalles para: {name}")

            print(f"[INFO] Pokémon aleatorios cargados en {time.time() - start:.2f} segundos")

        except Exception as e:
            print(f"[ERROR] Error al cargar Pokémon aleatorios: {e}")
            self.view.show_error(f"Error al cargar Pokémon: {str(e)}")

    def show_pokemon_details(self, pokemon):
        """Muestra los detalles del Pokémon seleccionado"""
        print(f"[DEBUG] Mostrando detalles de: {pokemon['name']} (ID: {pokemon['id']})")
        self.view.show_pokemon_details(pokemon)

    def get_pokemon_image(self, name):
        """Obtiene la imagen de un Pokémon (para uso interno)"""
        print(f"[DEBUG] Solicitando imagen de: {name}")
        pokemon = self.model.get_pokemon_details(name)
        return pokemon['image'] if pokemon else None
    def get_pokemon_list(self):
        """Obtiene la lista de Pokémon disponibles"""
        print("[DEBUG] Obteniendo lista de Pokémon")
        return self.model.get_pokemon_list()