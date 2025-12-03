from adventura.player import Player
from adventura.room import Room

class Hra:
    def __init__(self, player, rooms):
        self._player = player
        self._rooms = rooms

    @classmethod
    def from_dict(cls, data):
        player = Player.from_dict(data['player'])
        rooms = {room["room_id"]: Room.from_dict(room) for room in data['rooms']}
        return cls(player, rooms)

    @property
    def player(self):
        return self._player

    def active_room(self):
        return self._rooms[self.player.room_id]

    def game_over(self):
        room = self.active_room()
        return room.game_over

    def _replace(self, to_replace):
        room = self.active_room()
        new_exits = to_replace.get('exits', [])
        if new_exits:
            room.replace_exits(new_exits)
        new_desc = to_replace.get('desc', None)
        if new_desc:
            room.replace_desc(new_desc)

    def go(self, direction):
        room = self.active_room()
        exit = room.exit(direction)
        new_room_id = exit['room_id']
        self.player.room_id = new_room_id

    def take_item(self, item_id):
        room = self.active_room()
        player = self.player
        item = room.get_item(item_id)
        player.put_item(item_id, item)
        room.del_item(item_id)

    def use_item(self, item_id):
        room = self.active_room()
        player = self.player
        if player.has_item(item_id):
            use = room.item_use(item_id)
            to_replace = use.get('replace', {})
            self._replace(to_replace)
            player.del_item(item_id)
            return use.get("desc")
        else:
            raise ValueError("Neviem použiť " + item_id)


def test():
    test_hra = Hra.from_dict({"player": {"start_room_id": "1"},
                              "rooms": [{"room_id": "1",
                                         "label": "Čistinka",
                                         "desc": "Stojíš na kraji čistinky",
                                         "uses": [{
                                             "item_id": "maceta",
                                             "desc": "Použil si mačetu",
                                             "replace": {
                                                 "desc": "Rozsekaná čistinka",
                                                 "exits": [{
                                                     "label": "zapad",
                                                     "room_id": "10"
                                                 }]}}],
                                         "items": [{
                                             "label": "maceta",
                                             "desc": "Stará mačeta"
                                         }],
                                         "exits": []}]})
    assert test_hra.player.room_id == "1"
    assert test_hra.active_room().label == "Čistinka"
    test_hra.take_item("maceta")
    assert test_hra.active_room().items == []
    assert test_hra.player.inventory == ["maceta"]
    test_hra.use_item("maceta")
    assert test_hra.player.inventory == []
    assert test_hra.active_room().desc == "Rozsekaná čistinka"
    assert test_hra.active_room().exits == ["zapad"]
    test_hra.go("zapad")
    assert test_hra.player.room_id == "10"
    print("hra module test OK")

if __name__ == '__main__':
    test()
