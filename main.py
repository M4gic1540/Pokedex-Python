## main.py
# Main file to run the Pokémon application

import tkinter as tk
from pokemon_controller import PokemonController

def main():
    root = tk.Tk()
    app = PokemonController(root)
    root.mainloop()

if __name__ == "__main__":
    main()