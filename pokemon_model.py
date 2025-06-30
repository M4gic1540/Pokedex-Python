import time
import requests


class PokemonModel:
    TYPE_TRANSLATIONS = {
        "normal": "Normal",
        "fire": "Fuego",
        "water": "Agua",
        # ... (agrega los demás tipos si es necesario)
    }

    @staticmethod
    def log_duration(start_time, operation_name):
        elapsed = time.time() - start_time
        print(f"[DEBUG] {operation_name} completado en {elapsed:.2f} segundos")

    @staticmethod
    def get_json_with_timing(url, operation_name="Petición API"):
        start = time.time()
        print(f"[DEBUG] Iniciando {operation_name}: {url}")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        PokemonModel.log_duration(start, operation_name)
        return data

    @staticmethod
    def get_pokemon_list(limit=10):
        """Obtiene la lista de Pokémon de la API"""
        try:
            url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
            data = PokemonModel.get_json_with_timing(url, "Obtener lista de Pokémon")

            pokemons = [pokemon["name"] for pokemon in data.get("results", [])]
            print(f"[INFO] Se obtuvieron {len(pokemons)} Pokémon")
            return pokemons
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error al obtener lista de Pokémon: {e}")
            return []

    @staticmethod
    def get_pokemon_details(name, shiny=False, evolutions=False):
        try:
            start = time.time()
            url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
            data = PokemonModel.get_json_with_timing(
                url, f"Detalles de Pokémon: {name}"
            )

            species_url = data["species"]["url"]

            stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
            moves = [
                move["move"]["name"].replace("-", " ").title() for move in data["moves"]
            ]

            result = {
                "name": data["name"],
                "image": (
                    data["sprites"]["front_shiny"]
                    if shiny
                    else data["sprites"]["front_default"]
                ),
                "shiny": shiny,
                "types": [
                    PokemonModel.TYPE_TRANSLATIONS.get(
                        t["type"]["name"], t["type"]["name"]
                    )
                    for t in data["types"]
                ],
                "height": data["height"],
                "weight": data["weight"],
                "id": data["id"],
                "stats": stats,
                "moves": moves[:10],
                "evolutions": [],
                "evolution_species_url": species_url,
            }

            if evolutions:
                result["evolutions"] = PokemonModel.get_pokemon_evolution_chain(species_url)

            PokemonModel.log_duration(start, f"Procesamiento completo de {name}")
            return result

        except requests.exceptions.HTTPError:
            print(f"[ERROR] Pokémon '{name}' no encontrado (404).")
            return None
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error en la petición de {name}: {e}")
            return None

    @staticmethod
    def get_pokemon_evolution_chain(species_url):
        try:
            print(f"[DEBUG] Iniciando Especie de Pokémon: {species_url}")
            start = time.time()
            species_data = requests.get(species_url).json()
            print(
                f"[DEBUG] Especie de Pokémon completado en {time.time() - start:.2f} segundos"
            )

            evolution_url = species_data["evolution_chain"]["url"]
            print(f"[DEBUG] Iniciando Evolución de Pokémon: {evolution_url}")
            start = time.time()
            evolution_data = requests.get(evolution_url).json()
            print(
                f"[DEBUG] Evolución de Pokémon completado en {time.time() - start:.2f} segundos"
            )

            evolutions = []
            current = evolution_data["chain"]
            while current:
                evolutions.append(current["species"]["name"])
                current = current["evolves_to"][0] if current["evolves_to"] else None

            return evolutions
        except Exception as e:
            print(f"[ERROR] Error al obtener evolución: {e}")
            return []
