class Player:
    def __init__(self, start_room_id):
        self._room_id = start_room_id
        self._inventory = {}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @property
    def room_id(self):
        return self._room_id

    @room_id.setter
    def room_id(self, room_id):
        self._room_id = room_id

    @property
    def inventory(self):
        return list(self._inventory.keys())

    def put_item(self, item_id, item):
        self._inventory[item_id] = item

    def del_item(self, item_id):
        del self._inventory[item_id]

    def has_item(self, item_id):
        return item_id in self._inventory

def test():
    test_player = Player.from_dict({"start_room_id": 1})
    test_player.room_id = 2
    assert test_player.room_id == 2
    test_player.put_item("kluc", {
          "label": "kluc",
          "desc": "Zdobený kľúč"
        })
    assert test_player.has_item("kluc")
    assert test_player.inventory == ["kluc"]
    test_player.del_item("kluc")
    assert test_player.has_item("kluc") == False
    print("player module test OK")

if __name__ == '__main__':
    test()