# Choose Your Own Adventure Game
# Practice using functions, loops, conditions, lists, dictionaries, and randomization.
# Includes branching paths, combat, inventory, puzzles, and multiple endings.
# Also practices recursion, caching, and game-state logic.

import random
from functools import lru_cache


def is_fair_encounter(
    player_health,
    dragon_health,
    sword_count,
    shield_count,
    dragon_damage,
    sword_damage,
    shield_reduction
):
    
    @lru_cache(None)
    def check(
        health,
        dragon_hp,
        swords,
        shields,
        shield_active,
        player_turns_left,
        dragon_turns_left
    ):
        if dragon_hp <= 0:
            return True

        if health <= 0:
            return False

        if player_turns_left == 0 and dragon_turns_left == 0:
            return False

        possible_results = []

        # Player turn
        if player_turns_left > 0:

            player_can_win = False

            # Use sword
            if swords > 0:
                result = check(
                    health,
                    max(0, dragon_hp - sword_damage),
                    swords - 1,
                    shields,
                    shield_active,
                    player_turns_left - 1,
                    dragon_turns_left
                )

                if result:
                    player_can_win = True

            # Use shield
            if shields > 0:
                result = check(
                    health,
                    dragon_hp,
                    swords,
                    shields - 1,
                    True,
                    player_turns_left - 1,
                    dragon_turns_left
                )

                if result:
                    player_can_win = True

            possible_results.append(player_can_win)

        # Dragon turn
        if dragon_turns_left > 0:

            if shield_active:
                damage = max(
                    0,
                    dragon_damage - shield_reduction
                )
            else:
                damage = dragon_damage

            new_health = max(
                0,
                health - damage
            )

            result = check(
                new_health,
                dragon_hp,
                swords,
                shields,
                False,
                player_turns_left,
                dragon_turns_left - 1
            )

            possible_results.append(result)

        return all(possible_results)

    return check(
        player_health,
        dragon_health,
        sword_count,
        shield_count,
        False,
        5,
        5
    )


def generate_encounter():

    for attempt in range(1000):

        player_health = random.choice([90, 100])
        dragon_health = random.choice([90, 100])

        sword_count = 4
        shield_count = random.choice([1, 2])

        dragon_damage = random.choice([25, 30])
        sword_damage = 30
        shield_reduction = 20

        turns = ["player"] * 5 + ["dragon"] * 5
        random.shuffle(turns)

        if is_fair_encounter(
            player_health,
            dragon_health,
            sword_count,
            shield_count,
            dragon_damage,
            sword_damage,
            shield_reduction
        ):

            return {
                "turns": turns,
                "player_health": player_health,
                "dragon_health": dragon_health,
                "sword_count": sword_count,
                "shield_count": shield_count,
                "dragon_damage": dragon_damage,
                "sword_damage": sword_damage,
                "shield_reduction": shield_reduction
            }

    return {
        "turns": [
            "dragon",
            "player",
            "dragon",
            "player",
            "player",
            "dragon",
            "player",
            "dragon",
            "player",
            "dragon"
        ],
        "player_health": 100,
        "dragon_health": 90,
        "sword_count": 4,
        "shield_count": 2,
        "dragon_damage": 25,
        "sword_damage": 30,
        "shield_reduction": 20
    }


def dragon_battle():

    encounter = generate_encounter()

    turns = encounter["turns"]

    player_health = encounter["player_health"]
    dragon_health = encounter["dragon_health"]

    sword_count = encounter["sword_count"]
    shield_count = encounter["shield_count"]

    dragon_damage = encounter["dragon_damage"]
    sword_damage = encounter["sword_damage"]
    shield_reduction = encounter["shield_reduction"]

    shield_active = False

    print()
    print("=============================")
    print("       DRAGON BATTLE")
    print("=============================")

    print()
    print("Your health:", player_health)
    print("Dragon health:", dragon_health)
    print()
    print("Swords:", sword_count)
    print("Shields:", shield_count)
    print()
    print("The battle begins!")

    for turn in turns:

        if player_health <= 0:
            return False

        if dragon_health <= 0:
            return True

        # PLAYER TURN
        if turn == "player":

            print()
            print("-----------------------------")
            print("YOUR TURN")
            print("-----------------------------")

            print()
            print("Your health:", player_health)
            print("Dragon health:", dragon_health)
            print("Swords:", sword_count)
            print("Shields:", shield_count)
            print()
            print("1. Sword")
            print("2. Shield")

            while True:

                choice = input(
                    "Choose your action: "
                ).lower()

                if (
                    choice == "1"
                    or choice == "sword"
                ):

                    if sword_count <= 0:
                        print("You have no swords left!")
                        continue

                    dragon_health -= sword_damage
                    sword_count -= 1

                    print()
                    print( "You attack the dragon with your sword!")
                    print( "Dragon takes",sword_damage,"damage.")
                    print("Dragon health:",max(0, dragon_health))
                                              
                    break

                elif (
                    choice == "2"
                    or choice == "shield"
                ):

                    if shield_count <= 0:
                        print("You have no shields left!")
                        continue

                    shield_count -= 1
                    shield_active = True

                    print()
                    print("You raise your shield and prepare for the dragon's attack!")

                    break

                else:
                    print( "Invalid choice.Choose sword or shield.")

            if dragon_health <= 0:

                print()
                print("=============================")
                print("YOU DEFEATED THE DRAGON!")
                print("=============================")

                return True

        # DRAGON TURN
        elif turn == "dragon":

            print()
            print("-----------------------------")
            print("DRAGON'S TURN")
            print("-----------------------------")

            if shield_active:

                damage = max( 0, dragon_damage - shield_reduction)
                print()
                print("Your shield blocks part of the dragon's attack!")

                shield_active = False

            else:
                damage = dragon_damage

            player_health -= damage

            print()
            print("The dragon attacks!")
 

            print( "You take", damage, "damage.")
            print("Your health:",max(0, player_health))
                            
            if player_health <= 0:

                print()
                print("=============================")
                print("YOU WERE DEFEATED!")
                print("=============================")

                return False

    print()
    print("The battle ended.")
    print("GAME OVER")

    return False


def bridge():

    print()
    print("=============================")
    print("       THE OLD BRIDGE")
    print("=============================")

    print()
    print("You arrive at an old wooden bridge.")

    print()
    print("1. Cross the bridge")
    print("2. Turn back")

    choice = input( "What do you want to do? " ).lower()
       
    if choice in ("1", "cross"):
        print()
        print("You slowly step onto the bridge..."  )
        print( "The wooden boards begin to shake!")
  
        print()
        print("1. Keep moving")
        print("2. Turn back")

        second_choice = input( "What do you do? ").lower()
           
        if ( second_choice == "1" or second_choice in ("keep","continue" ) ):

            print()
            print("You keep moving forward." )
            print("The bridge shakes violently..." )
            print("but you finally reach the other side!")
                
            print()
            print("You look ahead and see something you weren't expecting...")

            print()
            print("🏰 A MASSIVE CASTLE 🏰")

            print()
            print("The castle gates stand before you.")

            return "castle"

        elif (
            second_choice == "2"
            or second_choice in (
                "back",
                "turn back"
            )
        ):

            print()
            print("You try to turn back...")
            print( "But the old bridge collapses!")
            print("You fall into the river.")
            print("GAME OVER")

            return "game_over"

        else:

            print()
            print("Invalid choice.")
            print("You hesitate for too long...")
            print("GAME OVER")

            return "game_over"

    elif (
        choice == "2"
        or choice in (
            "back",
            "turn back"
        )
    ):

        print()
        print( "You decide not to cross the bridge.")     
        print("You turn around and walk back into the forest.")
        print()
        print( "You eventually find a safe path home.")
        print()
        print("YOU ESCAPED!")

        return "escaped"

    else:

        print()
        print("Invalid choice.")
        print("GAME OVER")

        return "game_over"


def castle(inventory):

    print()
    print("=============================")
    print("         THE CASTLE")
    print("=============================")

    print()
    print("You stand before the enormous castle gates.")
    print("The gates slowly open...")
    print()
    print("You step inside.")
    print( "The castle is dark and silent.")
 
    while True:

        print()
        print("=============================")
        print("        CASTLE MENU")
        print("=============================")

        print()
        print("1. Explore the main hall")
        print("2. Go upstairs")
        print("3. Check inventory")

        choice = input("What do you want to do? " ).lower()
        
        # MAIN HALL
        if choice == "1" or choice in ("main hall", "hall"):

            print()
            print("-----------------------------")
            print("        MAIN HALL")
            print("-----------------------------")

            print()
            print("Dust covers the old furniture.")
            print("You slowly look around.")
            print()
            print("Near the fireplace,something catches your eye.")

            if "old key" not in inventory:

                print()
                print("🔑 You found an OLD KEY!")

                inventory.append("old key")

                print()
                print("You put the key in your pocket.")

            else:

                print()
                print("You have already searched the fireplace.")
                print("There is nothing else here.")

            print()
            print("Inventory:", inventory)
            print()
            print("You notice a large locked door upstairs.")
            print("Maybe this key opens it...")

        # UPSTAIRS
        elif choice in ("2", "back", "turn back"):

            print()
            print("-----------------------------")
            print("         UPSTAIRS")
            print("-----------------------------")

            print()
            print("You slowly climb the staircase.")
            print("Each step makes a loud creaking sound.")
            print()
            print("At the end of the corridor, you find a locked door.")

            if "old key" in inventory:

                print()
                print("You remember the old key you found downstairs.")
                print()
                print("You take the key from your pocket.")
                print("You unlock the door...")
                print()
                print("CLICK!")
                print()
                print("The door slowly opens.")
                print()
                print( "Something important lies beyond it...")
                print()
                print("You step into a mysterious room.")
                print("The door closes behind you.")

                print()
                print("=============================")
                print("       THE SECRET ROOM")
                print("=============================")

                print()
                print("Three ancient doors stand in front of you.")
                print()
                print("A strange message is written on the wall:")
                print()
                print('"Only one door leads forward."')
                print()
                print("1. The door with a lion")
                print("2. The door with a crown")
                print("3. The door with a snake")

                secret_choice = input( "Which door do you choose? ").lower()
              
                if secret_choice == "2" or secret_choice == "crown":

                    print()
                    print("You choose the door with the crown.")
                    print()
                    print("For a moment, nothing happens.")
                    print("Then you hear a deep CLICK.")
                    print()
                    print("The door slowly opens.")
                    print()
                    print("You chose correctly.")
                    print("A hidden staircase appears behind the door.")

                    print("=============================")
                    print("      CHALLENGE COMPLETE")
                    print("=============================")
                    print()
                    print("Your adventure continues...")
                    print()
                    print("You step through the doorway.")
                    print("Behind you, the door slowly closes.")
                    print()
                    print("You notice a hidden staircase.")
                    print("It leads deep beneath the castle.")
                    print()
                    print("You take a deep breath and begin walking down.")

                    print("=============================")
                    print("         THE DUNGEON")
                    print("=============================")

                    print()
                    print("The staircase finally ends.")
                    print("You find yourself in a cold, dark dungeon.")
                    print()
                    print("There is an old table in the corner.")
                    print("Something is lying on it.")
                    print()
                    print("🔑 You found a DUNGEON KEY!")

                    if "dungeon key" not in inventory:
                        inventory.append("dungeon key")

                    print()
                    print("You put the key in your pocket.")

                    print()
                    print("Your current inventory:")
                    for item in inventory:
                        print("-", item)

                    print()
                    print("At the other end of the dungeon,")
                    print("you see a large iron door.")
                    print()
                    print("A small keyhole is visible on the door.")
                    print()
                    print("You take out the dungeon key...")
                    print("CLICK!")
                    print()
                    print("The iron door unlocks.")
                    print()
                    print("You slowly push it open.")
                    print()
                    print("A bright light shines through the doorway.")
                    print()
                    print("=============================")
                    print("        THE FINAL ROOM")
                    print("=============================")
                    print()
                    print("You step through the iron door.")
                    print("The door closes behind you.")
                    print()
                    print("In front of you stands a mysterious stone pedestal.")
                    print("On it are three glowing symbols:")
                    print()
                    print("1. Sword")
                    print("2. Shield")
                    print("3. Crown")
                    print()
                    print("A message appears on the wall:")
                    print()
                    print('"Only one symbol will open the way out."')

                    final_choice = input("Which symbol do you choose? ").lower()
                        
                    if final_choice == "3" or final_choice == "crown":

                        print()
                        print("You place your hand on the crown.")
                        print()
                        print("The entire room begins to shake.")
                        print()
                        print("A hidden doorway opens in the wall.")

                        print()
                        print("=============================")
                        print("          YOU WIN!")
                        print("=============================")

                        print()
                        print("You have escaped the castle.")
                        print("You survived the dragon, crossed the bridge,")
                        print("solved the castle's mysteries, and reached the exit.")
                        print()
                        print("Congratulations, adventurer!")

                        return "win"

                    else:

                        print()
                        print("You choose the wrong symbol.")
                        print()
                        print("The room suddenly goes dark.")

                        print()
                        print("=============================")
                        print("         GAME OVER")
                        print("=============================")

                        return "game_over"

                else:

                    print()
                    print("You open the door...")
                    print()
                    print("A loud alarm echoes through the castle!")
                    print()
                    print("You chose the wrong door.")

                    print()
                    print("=============================")
                    print("          GAME OVER")
                    print("=============================")

                    return "game_over"

            else:

                print()
                print("The door is locked.")
                print("You don't have anything that can open it.")
                print()
                print("Maybe you should explore the main hall first.")

        # INVENTORY
        elif (
            choice == "3"
            or choice in ("inventory","items","bag")
         ):

            print()
            print("-----------------------------")
            print("         INVENTORY")
            print("-----------------------------")

            if inventory:

                for item in inventory:
                    print("-", item)

            else:

                print("Your inventory is empty.")
 
        else:

            print()
            print("Invalid choice.")


def main():

    name = input("Hey type your name: ")

    print( "Hello, " + name + "!")
    print("Welcome to my game!!")
 
    should_we_play = input( "Do you want to play a game? (yes/no): ").lower()
       
    if should_we_play in ("yes", "y"):

        print()
        print("Great! Let's start the game.")

        direction = input("Do you want to go left or right? (left/right): " ).lower()

        if direction == "left":

            print()
            print("You walk into the forest...")
            print( "Suddenly, a dragon appears!")

            result = dragon_battle()

            if result:

                print()
                print( "You survived the dragon battle!")

                result = bridge()

                if result == "castle":
                    inventory = []
                    castle(inventory)

        elif direction == "right":

            print()
            print( "You walk to the right...")
            print( "You see a bridge.")

            choice = input("Do you want to cross it or go back? (cross/back): ").lower()

            if choice == "cross":
                print()
                print( "You crossed the bridge!")
                print("You found a hidden treasure!")
                print("YOU WIN!")

            elif choice == "back":
                print()
                print("You went back into the forest.")
                print("GAME OVER")

            else:

                print()
                print("Invalid choice.")
                print("GAME OVER")

        else:

            print()
            print("Invalid choice.")
            print("GAME OVER")

    else:

        print()
        print("No worries! Maybe next time.")

main()