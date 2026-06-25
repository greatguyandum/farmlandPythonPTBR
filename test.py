import sys

# Define the map structure using a dictionary of rooms
game_map = {
    "cabin_living_room": {
        "description": "You are in a dimly lit cabin. The air is damp. A crucifix hangs upside down on the wall.",
        "exits": {"north": "cabin_hallway", "east": "cabin_kitchen"},
        "items": ["flashlight"]
    },
    "cabin_kitchen": {
        "description": "Flies buzz around rotting food. A rusty knife lies on the counter.",
        "exits": {"west": "cabin_living_room"},
        "items": ["knife"]
    },
    "cabin_hallway": {
        "description": "A narrow hallway. You hear scratching sounds behind the wallpaper.",
        "exits": {"south": "cabin_living_room", "north": "forest_entrance"},
        "items": []
    },
    "forest_entrance": {
        "description": "The wind howls through the dead trees. Mortis.",
        "exits": {"south": "cabin_hallway"},
        "items": []
    }
}

def game_loop():
    # Initialize the player's starting state
    current_room = "cabin_living_room"
    inventory = []
    
    print("M O R T I S\n" + "="*20)

    while True:
        room_data = game_map[current_room]
        
        # 1. Display room information
        print(f"\n{room_data['description']}")
        
        if room_data["items"]:
            print(f"You see here: {', '.join(room_data['items'])}")
            
        print(f"Exits: {', '.join(room_data['exits'].keys())}")
        
        # 2. Get user input
        command = input("\nWhat will you do? > ").strip().lower().split()
        
        if not command:
            continue
            
        action = command[0]
        
        # 3. Process actions
        if action in ["go", "move"]:
            if len(command) < 2:
                print("Go where?")
                continue
            direction = command[1]
            if direction in room_data["exits"]:
                current_room = room_data["exits"][direction]
            else:
                print("You cannot go that way.")
                
        elif action in ["get", "take"]:
            if len(command) < 2:
                print("Take what?")
                continue
            item = command[1]
            if item in room_data["items"]:
                room_data["items"].remove(item)
                inventory.append(item)
                print(f"You picked up the {item}.")
            else:
                print("That item is not here.")
                
        elif action in ["inventory", "i"]:
            if inventory:
                print(f"Your inventory: {', '.join(inventory)}")
            else:
                print("Your inventory is empty.")
                
        elif action in ["quit", "exit"]:
            print("Goodbye.")
            sys.exit()
            
        else:
            print("Unknown command. Try 'go [direction]', 'take [item]', or 'inventory'.")

if __name__ == "__main__":
    game_loop()
