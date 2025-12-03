from adventura.engine import Engine

nova_hra_file = "assets/hra.json"

engine = Engine.load_game(nova_hra_file)

engine.play()
