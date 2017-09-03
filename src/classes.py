# Built-in libraries
from copy import deepcopy
from abc import ABCMeta, abstractmethod

# 3rd-party libraries
import toml

# Local libraries
from settings import *
from mixins import *

class Item(ReprMixin, TomlDataMixin):

    """ Class for generating item objects; used by Inventory and Player """

    EQUIPMENT = ('weapon',
                 'helmet',
                 'chest',
                 'legs',
                 'shield',)

    def __init__(self, id_num: int):
        item_data = self.get_item_by_ID(id_num)
        self.name = item_data['name']
        self.slot = item_data['type']
        if self.slot in self.EQUIPMENT:
            self.attack = item_data.get('atk', None)
            self.defence = item_data.get('def', None)
            self.specialAttack = item_data.get('specialAttack', None)

class Inventory(ReprMixin):

    ITEMS_LIMIT = 28
    GEAR_SLOTS = {
        "weapon": None,
        "helmet": None,
        "chest":  None,
        "legs":   None,
        "shield": None,
        }

    def __init__(self, gear=None, items=None):
        if gear is None:
            self.gear = deepcopy(self.GEAR_SLOTS)
        else: #TODO: Check for validity
            self.gear = gear

        if items is None:
            self.items = []
        elif len(items) <= self.ITEMS_LIMIT:
            self.items = items
        else:
            raise ValueError(f"Number of items exceeded pre-set limit: {len(items)} > {self.ITEMS_LIMIT}")

        self.itemcount = len(self.items)

    def __len__(self):
        return self.itemcount

    def append(self, item: Item):
        if self.itemcount < self.ITEMS_LIMIT:
            self.items.append(item)
            self.itemcount += 1
        else:
            print("No room in inventory")

    def remove(self, item: Item):
        try:
            self.items.remove(item)
            self.itemcount -= 1
        except ValueError:
            print(f"You don't have any {item.name}s")

    def equip(self, item_index: int):
        """ Equip an item from inventory at the specified index. """
        try:
            item = self.items[item_index] # Find the item to be equipped
            temp = self.gear[item.slot]   # Temporarily store the currently equipped item (if any)
            self.gear[item.slot] = item   # Equip item
            self.remove(item)             # Remove equipped item from inventory
            if temp is not None:
                self.append(temp)
                print(f"You swapped {temp.name} to {item.name}")
            else:
                print(f"You equip {item.name}")
        except KeyError:
            print("You can't equip that")
        except IndexError:
            print("There's nothing in that inventory space")

    def unequip(self, slot: str):
        if self.gear[slot] is not None:
            self.append(self.gear[slot])
            self.gear[slot] = None
            print(f"You unequip {self.items[-1].name}")
        else:
            print("That slot is empty")

class Player(ReprMixin):
    def __init__(self, name, level=1, inventory=None):
        self.name = name
        self.level = level
        if inventory is None:
            self.inventory = Inventory()
        else:
            self.inventory = inventory

def test():
    sword = Item(0)
    bag_of_pebbles = [Item(1) for i in range(30)]
    helmet = Item(2)
    player = Player("Bob")
    print(player)
    print(f"Player is carrying {player.inventory.itemcount} items")
    player.inventory.append(sword)
    print(player)
    player.inventory.unequip('weapon')
    print(player)
    player.inventory.equip(player.inventory.items.index(sword))
    print(player)
    player.inventory.unequip('weapon')
    print(player)
    for pebble in bag_of_pebbles:
        print(f"Player is carrying {player.inventory.itemcount} items")
        player.inventory.append(pebble)
    player.inventory.remove(helmet)


if __name__ == "__main__":
    test()
