import json
import sys
import random
import doctest


class Game:
    def __init__(player, map):
        player.map = map
        player.gameArea = None
        player.location = None
        player.inventory = []
        player.equippedItem = None

    def checkMap(player):
        try:
            with open(player.map, 'r') as file:
                player.gameArea = json.load(file)
            if not player.validate_map():
                sys.exit("Invalid game map.")
        except Exception as e:
            sys.stderr.write(str(e))
            sys.exit(1)

    def validate_map(player):
        if 'start' not in player.gameArea or 'rooms' not in player.gameArea:
            return False
        room_names = {room['name'] for room in player.gameArea['rooms']}
        if len(room_names) != len(player.gameArea['rooms']):
            return False
        validMap = all(room['name'] in room_names for room in player.gameArea['rooms']
                       for exit in room['exits'].values())
        return validMap

    def setGame(player):
        player.location = player.gameArea['start']
        roomDetails = player.findRoom(player)
        if roomDetails:
            player.roomInfo(roomDetails)
        player.GLoop()

    def GLoop(player):
        while True:
            try:
                text = input("What would you like to do? ").strip().lower()
                if text == 'quit':
                    print("Goodbye!")
                    break
                player.playInput(text)
            except EOFError:
                print("Use 'quit' to exit.")

    def playInput(player, inputText):
        parts = inputText.split()
        if not parts:
            print("if you need helps see ReadME")
            return

        if parts[0] == 'go':
            if len(parts) < 2:
                print("Sorry, you need to 'go' somewhere.")
            else:
                player.move(parts[1])
        elif parts[0] == 'look':
            player.look()
        elif parts[0] == 'get':
            if len(parts) < 2:
                print("Sorry, you need to 'get' something.")
            else:
                player.getFunction(parts[1])
        elif parts[0] == 'drop':
            if len(parts) < 2:
                print("Sorry, you need to 'drop' something.")
            else:
                player.dropFunction(parts[1])
        elif parts[0] == 'inventory':
            player.inventoryFunction()
        elif parts[0] == 'equip':
            if len(parts) < 2:
                print("Sorry, you need to 'equip' something.")
            else:
                player.equipFunction(parts[1])
        elif parts[0] == 'attack':
            player.attack()
        elif parts[0] == 'enhance':
            player.enhance()
        elif parts[0] == 'check':
            player.checkFunction()
        else:
            print(f"Use 'quit' to exit.")

    def findRoom(player, room):
        for room in player.gameArea['rooms']:
            if room['name'] == player.location:
                return room
        return None

    def look(player):
        roomDetails = player.findRoom(player)
        if roomDetails:
            player.roomInfo(roomDetails)

    def roomInfo(player, room):
        print(f"> {room['name']}\n")
        print(f"{room['desc']}\n")
        exits = ' '.join(room['exits'])
        if 'items' in room and room['items']:
            items = ' '.join(room['items'])
            print(f"Items: {items}\n")
        print(f"Exits: {exits}\n")
        if 'monster' in room:
            print(
                f"Monster: {room['monster']['name']} (Health: {room['monster']['health']})\n")

    def move(player, D):
        roomDetails = player.findRoom(player)
        if D in roomDetails['exits']:
            player.location = roomDetails['exits'][D]
            newRoom = player.findRoom(player)
            if newRoom:
                print(f"You go {D}.\n")
                player.roomInfo(newRoom)
        else:
            print(f"There's no way to go {D}.")

    def getFunction(player, item):
        roomDetails = player.findRoom(player)
        if item in roomDetails.get('items', []):
            itemInfo = {'itemName': item,
                        'enhanceName': item, 'extraDamage': 0}
            player.inventory.append(itemInfo)
            roomDetails['items'].remove(item)
            print(f"You pick up the {item}.")
        else:
            print(f"There's no {item} anywhere.")

    def inventoryFunction(player):
        if player.inventory:
            print("Inventory:")
            for item in player.inventory:
                print(f"  {item['itemName']}")
        else:
            print("You're not carrying anything.")


# extension 1 drop

    def dropFunction(player, item):
        dropitem = next(
            (i for i in player.inventory if i['itemName'] == item), None)
        if dropitem:
            player.inventory.remove(dropitem)
            roomDetails = player.findRoom(player)
            roomDetails.get('items', []).append(item)
            print(f"You drop the {dropitem['itemName']}.")
            if dropitem == player.equippedItem:
                player.equippedItem = None
        else:
            print(f"You don't have a {item} to drop.")

# extension 2 equip item in the inventory
    def equipFunction(player, item):
        equipItem = next(
            (i for i in player.inventory if i['itemName'] == item), None)
        if equipItem:
            player.equippedItem = equipItem
            print(f"You have equipped the {equipItem['enhanceName']}.")
        else:
            print(f"You don't have a {item} to equip.")

    def checkFunction(player):
        if player.equippedItem:
            print(
                f"You have equipped: {player.equippedItem['enhanceName']} which gives {player.equippedItem['extraDamage']} extra damage")
        else:
            print("No item is currently equipped.")

# extension 3 gives items damage boost
    def enhance(player):
        roomDetails = player.findRoom(player)
        if 'token' in roomDetails and player.equippedItem:
            extraDamage = random.randint(1, 20)
            if extraDamage <= 5:
                tag = "common"
            elif extraDamage <= 10:
                tag = "rare"
            elif extraDamage <= 15:
                tag = "epic"
            else:
                tag = "legendary"

            tag2 = f"{tag} {player.equippedItem['itemName']}"
            player.equippedItem['enhanceName'] = tag2
            player.equippedItem['extraDamage'] = extraDamage
            print(
                f"You have enhanced your {tag2} to {extraDamage} attack power.")
        else:
            if not 'token' in roomDetails:
                print("There is no enhancement token in this room.")
            if player.equippedItem == None:
                print("You need to equip an item to enhance it.")

# extension 4 able to attack the monster
    def attack(player):
        roomDetails = player.findRoom(player)
        if 'monster' in roomDetails:
            basicDamge = random.randint(5, 10)
            if player.equippedItem == None:
                total_damage = basicDamge
            else:
                total_damage = player.equippedItem['extraDamage'] * basicDamge
            roomDetails['monster']['health'] -= total_damage
            print(
                f"You attack the {roomDetails['monster']['name']} and deal {total_damage} damage!")
            if roomDetails['monster']['health'] <= 0:
                print(f"The {roomDetails['monster']['name']} is defeated!")
                del roomDetails['monster']
        else:
            print("There is no monster in the room.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python3 adventure.py map.map")
        sys.exit(1)
    game = Game(sys.argv[1])
    game.checkMap()
    game.setGame()
