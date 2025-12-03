import json
import textwrap

from adventura.hra import Hra

class Engine:
    def __init__(self, hra, intro, outro):
        self._hra = hra
        self._intro = intro
        self._outro = outro

    def action(self):
        try:
            commands = input("Čo chceš urobiť?: ").split()
            verb = commands[0]
            noun = commands[1] if len(commands) > 1 else None
            if verb == "help":
                print()
                print("!!!!!!!!!!!! HELP !!!!!!!!!!!!!!!!!!!!")
                print("Pre ukončenie hry napíš exit")
                print("Z miestnosti sa vieš presunúť príkazom go a smer, ktorým sa chceš ubrať, napríklad go vychod.")
                print("Zobrať vec zo zeme vieš pomocou príkazu take a vec, ktorú chceš zobrať, napríklad take doska.")
                print("Použiť vec vieš príkazom use a vec, ktorú chceš použiť.")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            elif verb == "exit":
                return True
            elif verb == "go":
                self._hra.go(noun)
            elif verb == "take":
                self._hra.take_item(noun)
            elif verb == "use":
                desc = self._hra.use_item(noun)
                print()
                print("!!!!!!!!!!!! AKCIA !!!!!!!!!!!!!!!!!!!!")
                print(desc)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                self._hra.go(verb)
        except KeyboardInterrupt as ex:
            return True
        except Exception as ex:
            print()
            print("!!!!!!!!!!!! CHYBA !!!!!!!!!!!!!!!!!!!!")
            print("Nerozumiem príkazu. Ak si nevieš dať rady napíš help")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def intro(self):
        print(self._intro)
        input("Stlač Enter pre pokračovanie...")

    def game_over(self, msg):
        print()
        print("!!!!!!!!!!!! GAME OVER !!!!!!!!!!!!!!")
        print(msg)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(self._outro)

    def describe(self):
        room = self._hra.active_room()
        player = self._hra.player
        print()
        print("--------------------------------------------------------------------------")
        print("Nachádzaš sa:", room.label)
        print("--------------------------------------------------------------------------")
        print("\n".join(textwrap.wrap(room.desc, width=70)))
        print()
        if len(room.exits) > 0:
            print("Môžeš ísť:", ", ".join(room.exits))
        if len(room.items) > 0:
            print("Na zemi sa nachádza:", ", ".join(room.items))
        if len(player.inventory) > 0:
            print("V inventári máš:", ", ".join(player.inventory))
        print("--------------------------------------------------------------------------")

    def play(self):
        self.intro()
        while True:
            self.describe()
            game_over_msg = self._hra.game_over()
            if game_over_msg:
                self.game_over(game_over_msg)
                break
            should_quit = self.action()
            if should_quit:
                self.game_over("Vzdal si to skôr ako si stihol nájsť poklad!")
                break


    @classmethod
    def from_dict(cls, data):
        hra = Hra.from_dict(data)
        return cls(hra, data['intro'], data['outro'])

    @classmethod
    def load_game(cls, json_path):
        with open(json_path) as json_file:
            data = json.load(json_file)
            return Engine.from_dict(data)