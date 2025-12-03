class Room:
    def __init__(self, room_id, label, desc, items=None, uses=None, exits=None, game_over=None):
        if exits is None:
            exits = []
        if uses is None:
            uses = []
        if items is None:
            items = []
        self._room_id = room_id
        self._label = label
        self._desc = desc
        self._exits = {exit["label"]: exit for exit in exits}
        self._uses = {use["item_id"]: use for use in uses}
        self._items = {item["label"]: item for item in items}
        self._game_over = game_over

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @property
    def items(self):
        return list(self._items.keys())

    def get_item(self, item_id):
        return self._items[item_id]

    def del_item(self, item_id):
        del self._items[item_id]

    @property
    def exits(self):
        return list(self._exits.keys())

    def exit(self, direction):
        return self._exits[direction]

    def replace_exits (self, exits):
        self._exits = {exit["label"]: exit for exit in exits}

    def replace_desc (self, desc):
        self._desc = desc

    def item_use(self, item_id):
        return self._uses[item_id]

    @property
    def game_over(self):
        return self._game_over

    @property
    def desc(self):
        return self._desc

    @property
    def label(self):
        return self._label

def test():
    test_room = Room.from_dict({"room_id": "1",
                                "label": "Čistinka",
                                "desc": "Stojíš na kraji čistinky",
                                "items": [
                                    {
                                        "label": "kluc",
                                        "desc": "Zdobený kľúč"
                                    }
                                ],
                                "uses": [
                                    {
                                        "item_id": "kluc",
                                        "desc": "Kľúčom si odomkol dvere",
                                    }
                                ],
                                "exits": [{
                                    "label": "zapad",
                                    "room_id": "2"
                                }, {
                                    "label": "vychod",
                                    "room_id": "3"}]})
    assert test_room.label == "Čistinka"
    assert test_room.desc == "Stojíš na kraji čistinky"
    assert test_room.game_over is None
    assert test_room.exits == ["zapad", "vychod"]
    assert test_room.exit("zapad") == {
                                    "label": "zapad",
                                    "room_id": "2"}

    assert test_room.items == ["kluc"]
    assert test_room.get_item("kluc") == {
                                        "label": "kluc",
                                        "desc": "Zdobený kľúč"
                                    }
    test_room.del_item("kluc")
    assert test_room.items == []
    assert test_room.item_use("kluc") == {
                                        "item_id": "kluc",
                                        "desc": "Kľúčom si odomkol dvere",
                                    }
    test_room.replace_exits([{"label": "zapad",
                                    "room_id": "2"
                                }])
    test_room.replace_desc("Stojíš na kraji čistinky, prší")
    assert test_room.desc == "Stojíš na kraji čistinky, prší"
    assert test_room.exits == ["zapad"]
    print("room module test OK")

if __name__ == '__main__':
    test()
